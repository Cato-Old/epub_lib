class Paragraph:
    def __init__(self, input_str: str):
        if '\n' in input_str:
            raise ValueError
        self.content = input_str
