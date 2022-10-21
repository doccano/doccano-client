from typing import List, Literal

import numpy as np
from flair.data import Sentence
from seqal.tagger import SequenceTagger


def least_confidence(
    sentences: List[Sentence],
    tagger: SequenceTagger,
) -> np.ndarray:
    log_probs = tagger.log_probability(sentences)
    # scores = 1 - np.exp(log_probs)
    scores = np.exp(log_probs)
    return scores


def maximum_normalized_log_probability(
    sentences: List[Sentence],
    tagger: SequenceTagger,
) -> np.ndarray:
    log_probs = tagger.log_probability(sentences)
    lengths = np.array([len(sent) for sent in sentences])
    normed_log_probs = log_probs / lengths
    return normed_log_probs


def get_query_strategy(query_strategy: Literal["MNLP", "LC"] = "MNLP"):
    if query_strategy == "LC":
        return least_confidence
    elif query_strategy == "MNLP":
        return maximum_normalized_log_probability
    raise ValueError(f"Query strategy {query_strategy} is not available")
