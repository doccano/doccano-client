import json
import pathlib
import time
from typing import List, Literal, Optional, Tuple

import pandas as pd
from flair.trainers import ModelTrainer
from seqal.tagger import SequenceTagger
from tqdm import tqdm

from doccano_client import DoccanoClient

from .preparation import DOCCANO_HOME, prepare_datasets
from .strategies import get_query_strategy
from .trainer import get_tagger_params, get_trainer_params


def execute_one_iteration(
    client: DoccanoClient,
    project_id: int,
    lang: str = "en",
    query_strategy_name: Literal["LC", "MNLP"] = "MNLP",
    transformer_model: Optional[str] = None,
) -> Tuple[List[float], List[int], float]:
    print("Maybe downloading dataset...")
    labeled_dataset, unlabeled_dataset = prepare_datasets(client, project_id, lang=lang)

    # Prepare tagger
    tagger_params = get_tagger_params(labeled_dataset, lang=lang, transformer_model=transformer_model)
    tagger = SequenceTagger(**tagger_params)

    # Prepare trainer
    trainer = ModelTrainer(tagger, labeled_dataset)
    trainer_params = get_trainer_params()

    print("Training...")
    model_dir = DOCCANO_HOME / str(project_id) / "models"
    trainer.train(model_dir, **trainer_params)
    print("Training completed.")

    print("Evaluating...")
    result = tagger.evaluate(labeled_dataset.test, gold_label_type="ner")
    f1_micro = result.main_score
    print("Evaluation Completed.")

    # Query unlabeled dataset
    print("Calculating confidence scores...")
    query_strategy = get_query_strategy(query_strategy_name)
    scores = query_strategy(unlabeled_dataset.sentences, tagger)
    print("Calculation completed.")
    return scores, unlabeled_dataset.ids, f1_micro


def save_evaluation_result(project_id: int, number_of_data: List[int], scores: List[float]) -> pathlib.Path:
    eval_file = DOCCANO_HOME / str(project_id) / "models" / "evaluation.json"
    with eval_file.open(mode="w") as f:
        results = {"number_of_data": number_of_data, "scores": scores}
        f.write(json.dumps(results))
    return eval_file


def finish_active_learning(eval_file: pathlib.Path, patience: int) -> bool:
    with eval_file.open() as f:
        results = json.load(f)
    if patience < 0:
        return False
    max_score = max(results["scores"])
    max_score_index = results["scores"].index(max_score)
    current_score = results["scores"][-1]
    current_score_index = len(results["scores"]) - 1
    return current_score < max_score and current_score_index - max_score_index > patience


def show_results(eval_file: pathlib.Path):
    with eval_file.open() as f:
        results = json.load(f)
    df = pd.DataFrame(results)
    print(df.to_markdown(index=False))


def execute_active_learning(
    client: DoccanoClient,
    project_id: int,
    lang: str = "en",
    query_strategy_name: Literal["LC", "MNLP"] = "MNLP",
    transformer_model: Optional[str] = None,
    train_frequency: int = 50,
    patience: int = -1,
):
    prev_completed = 0
    number_of_data = []
    f1_scores = []
    while True:
        progress = client.get_progress(project_id)
        if progress.is_finished():
            break
        if progress.completed - prev_completed >= train_frequency:
            prev_completed = progress.completed
            scores, example_ids, f1_micro = execute_one_iteration(
                client,
                project_id=project_id,
                lang=lang,
                query_strategy_name=query_strategy_name,
                transformer_model=transformer_model,
            )
            print("Update confidence scores...")
            for score, example_id in tqdm(zip(scores, example_ids)):
                client.update_example(project_id, example_id, score=score)
            print("Update completed.")

            number_of_data.append(progress.completed)
            f1_scores.append(f1_micro)
            eval_file = save_evaluation_result(project_id, number_of_data, f1_scores)
            show_results(eval_file)
            if finish_active_learning(eval_file, patience):
                break
        time.sleep(10)
