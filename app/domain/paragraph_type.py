import re
from enum import Enum


class ParagraphType(Enum):
    CONTINUATION = (1, r'[^\$]', '<p>{content}</p>')
    INDENT = (2, r'\$>', '<p class="a2">{content}</p>')
    CHAPTER_HEADER = (4, r'\$h2>', '<h2>{content}</h2>')
    INDENT_QUOTE = (7, r'\$cyt>\$>', '<p class="cyt a2">{content}</p>')
    RIGHT_ALIGNED = (3, r'\$r>', '<p class="a2 r">{content}</p>')

    def __init__(self, ind, pattern, template):
        self.ind = ind
        self.pattern = pattern
        self.template = template


class ParagraphTypeRecognizer:
    @staticmethod
    def recognize(raw_text: str) -> ParagraphType:
        for paragraph_type in ParagraphType:
            marker = raw_text[0:paragraph_type.ind]
            if re.fullmatch(paragraph_type.pattern, marker):
                return paragraph_type
