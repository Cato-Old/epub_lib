import re
from enum import Enum
from string import Template


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

    def dump(self) -> str:
        return '\n'.join(par.dump() for par in self.paragraphs)

    def dump_to_file(self) -> None:
        with open('../resources/template.xhtml', 'r') as f:
            template = Template(f.read())
        with open(f'{self.number}.xhtml', 'w') as f:
            f.write(template.substitute(
                page_number=self.number, content=self.dump()
            ))


class Book:
    def __init__(self, path: str) -> None:
        with open(path, 'r') as file:
            raw_text = file.read()
        self.pages = self._build_pages_list(raw_text)

    def _build_pages_list(self, raw_text: str) -> list:
        lines = raw_text.split('\n')
        markers = [line for line in lines if re.fullmatch(r'Str\d{1,4}', line)]
        markers_indices = [raw_text.index(marker) for marker in markers]
        markers_indices.append(len(raw_text))
        raw_pages = []
        for begin, end in zip(markers_indices, markers_indices[1:]):
            end = end-1 if raw_text[end-1] == '\n' else end
            raw_pages.append(raw_text[begin:end])
        return [Page(raw_text) for raw_text in raw_pages]

    def dump(self) -> None:
        for page in self.pages:
            page.dump_to_file()

