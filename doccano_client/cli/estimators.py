from __future__ import annotations

from typing import Iterator

from doccano_client.cli.entity import Entity


class SpaCyEntityEstimator:
    def __init__(self, model: str):
        import spacy

        self.nlp = spacy.load(model)

    def predict(self, text: str) -> Iterator[Entity]:
        doc = self.nlp(text)
        for entity in doc.ents:
            yield Entity(start_char=entity.start_char, end_char=entity.end_char, label=entity.label_)


class ASREstimator:
    def __init__(self, model: str):
        import whisper

        self.recognizer = whisper.load_model(model)

    def predict(self, audio_file: str) -> str:
        result = self.recognizer.transcribe(audio_file)
        return result["text"]


def select_estimator_class(task: str, framework: str):
    if task == "ner" and framework == "spacy":
        return SpaCyEntityEstimator
    if task == "asr":
        return ASREstimator
    raise ValueError("There is no estimator.")
