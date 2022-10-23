import time
from typing import List, Literal, Optional, Tuple

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
) -> Tuple[List[float], List[int]]:
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

    # Query unlabeled dataset
    print("Calculating confidence scores...")
    query_strategy = get_query_strategy(query_strategy_name)
    scores = query_strategy(unlabeled_dataset.sentences, tagger)
    print("Calculation completed.")
    return scores, unlabeled_dataset.ids


def execute_active_learning(
    client: DoccanoClient,
    project_id: int,
    lang: str = "en",
    query_strategy_name: Literal["LC", "MNLP"] = "MNLP",
    transformer_model: Optional[str] = None,
    train_frequency: int = 100,
):
    prev_completed = 0
    while True:
        progress = client.get_progress(project_id)
        if progress.is_finished():
            break
        if progress.completed - prev_completed >= train_frequency:
            prev_completed = progress.completed
            scores, example_ids = execute_one_iteration(
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
        time.sleep(10)
