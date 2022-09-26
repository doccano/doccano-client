from __future__ import annotations


class Entity:
    def __init__(self, start_char: int, end_char: int, label: str):
        if start_char < 0 or end_char < 0:
            raise ValueError("The offset must be greater than or equal to 0")
        if start_char >= end_char:
            raise ValueError("The start offset must be less than the end offset")
        if label == "":
            raise ValueError("The label text must not be empty text.")
        self.start_char = start_char
        self.end_char = end_char
        self.label = label
