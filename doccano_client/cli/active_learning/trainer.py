from flair.data import Corpus
from flair.embeddings import TransformerWordEmbeddings, WordEmbeddings
from flair.trainers import ModelTrainer
from seqal.tagger import SequenceTagger

from .languages import LANGUAGES


def get_tagger_params(
    corpus: Corpus,
    lang: str = "en",
    transformer_model: str = None,
    hidden_size: int = 256,
    use_rnn: bool = False,
    use_crf: bool = True,
    **kwargs,
):
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
):
    trainer_params = {
        "max_epochs": max_epochs,
        "learning_rate": learning_rate,
        "mini_batch_size": mini_batch_size,
        "patience": patience,
        "shuffle": shuffle,
    }
    return trainer_params


def make_tagger(corpus: Corpus):
    tagger_params = get_tagger_params(corpus)
    tagger = SequenceTagger(**tagger_params)
    return tagger


def make_trainer(tagger: SequenceTagger, corpus: Corpus):
    trainer = ModelTrainer(tagger, corpus)
    return trainer


def train(tagger, trainer, dir_path):
    trainer_params = get_trainer_params()
    trainer.train(dir_path, **trainer_params)
    return tagger
