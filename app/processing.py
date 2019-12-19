from app.domain import ParagraphType


class ParagraphProcessor:
    @staticmethod
    def process(raw_text: str, paragraph_type: ParagraphType) -> str:
        if paragraph_type == ParagraphType.CONTINUATION:
            return raw_text
        else:
            return raw_text[paragraph_type.ind:]
