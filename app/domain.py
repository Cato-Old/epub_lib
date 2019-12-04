import re
from enum import Enum


class ParagraphType(Enum):
    CONTINUATION = (1, r'[^\$]', '<p>{content}</p>')
    INDENT = (2, r'\$>', '<p class="a2">{content}</p>')

    def __init__(self, ind, pattern, template):
        self.ind = ind
        self.pattern = pattern
        self.template = template


class Paragraph:
    def __init__(self, raw_text: str):
        if '\n' in raw_text:
            raise ValueError
        self.content = raw_text
        self.type = self._recognize_paragraph_type(raw_text)

    def _recognize_paragraph_type(self, raw_text: str) -> ParagraphType:
        for paragraph_type in ParagraphType:
            marker = raw_text[0:paragraph_type.ind]
            if re.fullmatch(paragraph_type.pattern, marker):
                return paragraph_type

