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

    def dump(self) -> str:
        return self.type.template.format(content=self.content)


class Page:
    def __init__(self, raw_text: str):
        self.number = self._extract_page_number(raw_text)
        self.paragraphs = self._build_paragraphs_list(raw_text)

    def _extract_page_number(self, raw_text: str) -> int:
        page_desc = raw_text.split('\n')[0]
        self._validate_page_description(page_desc)
        num_str = page_desc[3:]
        return int(num_str)

    def _validate_page_description(self, page_desc: str) -> None:
        if 'Str' != page_desc[:3]:
            raise ValueError(f'{page_desc} is not a page description')
        if not re.fullmatch(r'\d{1,4}', page_desc[3:]):
            raise ValueError(f'{page_desc[3:]} is not a page number')

    def _build_paragraphs_list(self, raw_text: str) -> list:
        raw_paragraphs = raw_text.split('\n')[1:]
        return [Paragraph(par) for par in raw_paragraphs]
