from typing import List, Literal

import numpy as np
from flair.data import Sentence
from seqal.tagger import SequenceTagger


def least_confidence(
    sentences: List[Sentence],
    tagger: SequenceTagger,
) -> np.ndarray:
    log_probs = tagger.log_probability(sentences)
    scores = 1 - np.exp(log_probs)
    return scores


def maximum_normalized_log_probability(
    sentences: List[Sentence],
    tagger: SequenceTagger,
) -> np.ndarray:
    log_probs = tagger.log_probability(sentences)
    lengths = np.array([len(sent) for sent in sentences])
    normed_log_probs = log_probs / lengths
    return normed_log_probs


def get_sampling_algorithm(sampler: Literal["MNLP", "LC"] = "MNLP"):
    if sampler == "LC":
        return least_confidence
    elif sampler == "MNLP":
        return maximum_normalized_log_probability
    raise ValueError(f"Sampler {sampler} is not available")
