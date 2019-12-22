import re

from app.domain.paragraph_type import ParagraphType


class ParagraphProcessor:
    @staticmethod
    def process(raw_text: str, paragraph_type: ParagraphType) -> str:
        text = ParagraphProcessor.process_type_marker(raw_text, paragraph_type)
        return ParagraphProcessor.process_italic_marker(text)

    @staticmethod
    def process_type_marker(
            raw_text: str, paragraph_type: ParagraphType,
    ) -> str:
        if paragraph_type == ParagraphType.CONTINUATION:
            return raw_text
        else:
            return raw_text[paragraph_type.ind:]

    @staticmethod
    def process_italic_marker(raw_text: str) -> str:
        return re.sub(r'€([^€<]+)€', lambda m: f'<i>{m.group(1)}</i>', raw_text)
