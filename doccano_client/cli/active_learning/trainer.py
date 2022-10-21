from typing import Any, Dict

from flair.data import Corpus
from flair.embeddings import TransformerWordEmbeddings, WordEmbeddings

from .languages import LANGUAGES


def get_tagger_params(
    corpus: Corpus,
    lang: str = "en",
    transformer_model: str = None,
    hidden_size: int = 256,
    use_rnn: bool = False,
    use_crf: bool = True,
    **kwargs,
) -> Dict[str, Any]:
    if lang not in LANGUAGES and transformer_model is None:
        raise ValueError(f"Language {lang} is not available")

    if transformer_model:
        embeddings = TransformerWordEmbeddings(transformer_model)
    else:
        embeddings = WordEmbeddings("glove")

    tagger_params = {
        "tag_type": "ner",
        "tag_dictionary": corpus.make_tag_dictionary(tag_type="ner"),
        "embeddings": embeddings,
        "hidden_size": hidden_size,
        "use_rnn": use_rnn,
        "use_crf": use_crf,
    }
    return tagger_params


def get_trainer_params(
    max_epochs: int = 10,
    patience: int = 3,
    learning_rate: float = 0.1,
    mini_batch_size: int = 32,
    shuffle: bool = True,
    **kwargs,
) -> Dict[str, Any]:
    trainer_params = {
        "max_epochs": max_epochs,
        "learning_rate": learning_rate,
        "mini_batch_size": mini_batch_size,
        "patience": patience,
        "shuffle": shuffle,
    }
    return trainer_params
