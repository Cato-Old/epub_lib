import re
from dataclasses import dataclass

from app.domain.paragraph_type import ParagraphType


@dataclass(frozen=True)
class ProcessedParagraph:
    text: str
    type: ParagraphType


class ParagraphProcessor:
    @staticmethod
    def process(paragraph: ProcessedParagraph) -> ProcessedParagraph:
        paragraph = ParagraphProcessor.process_type_marker(paragraph)
        return ParagraphProcessor.process_italic_marker(paragraph)

    @staticmethod
    def process_type_marker(
            paragraph: ProcessedParagraph,
    ) -> ProcessedParagraph:
        if paragraph.type == ParagraphType.CONTINUATION:
            return paragraph
        else:
            return ProcessedParagraph(
                text=paragraph.text[paragraph.type.ind:],
                type=paragraph.type,
            )

    @staticmethod
    def process_italic_marker(
            paragraph: ProcessedParagraph,
    ) -> ProcessedParagraph:
        text = re.sub(
            r'€([^€<]+)€',
            lambda m: f'<i>{m.group(1)}</i>',
            paragraph.text,
        )
        return ProcessedParagraph(text=text, type=paragraph.type)
