from random import randint, shuffle
from unittest import TestCase

from factory import Faker

from app.domain import ParagraphType
from app.processing import ParagraphProcessor, ProcessedParagraph
from tests.test_domain import PARAGRAPH_TEST_PARAMS


class ParagraphProcessorTest(TestCase):
    def setUp(self) -> None:
        self.processor = ParagraphProcessor()
        self.params = PARAGRAPH_TEST_PARAMS

    def test_processes_raw_text_type_marker(self) -> None:
        for tested_type, content, regex_content, _ in self.params:
            with self.subTest(tested_type):
                paragraph = ProcessedParagraph(content, tested_type)
                actual = self.processor.process(paragraph)
                self.assertRegex(actual.text, regex_content)

    def test_processes_raw_text_italic_markers(self) -> None:
        paragraph = ProcessedParagraph(
            text=self.sentence_with_italic(), type=ParagraphType.CONTINUATION,
        )
        actual = self.processor.process(paragraph)
        self.assertRegex(actual.text, r'.*<i>.+</i>.*')

    def test_processes_raw_text_widows(self) -> None:
        paragraph = ProcessedParagraph(
            text=self.sentence_with_widows(), type=ParagraphType.CONTINUATION,
        )
        actual = self.processor.process(paragraph)
        for widow in 'wiouza':
            with self.subTest(widow):
                self.assertNotRegex(actual.text, f' {widow} ')
                self.assertNotRegex(actual.text, f'{widow.upper()} ')

    def sentence_with_italic(self) -> str:
        words = Faker('words', nb=randint(1, 10)).generate()
        ind = randint(0, len(words)-1)
        words[ind] = f'€{words[ind]}€'
        words[0] = words[0].title()
        return ' '.join(words) + '.'

    def sentence_with_widows(self) -> str:
        words = Faker('words', nb=randint(10, 20)).generate()
        words.extend('wiouza')
        while words[-1] in 'wiouza':
            shuffle(words)
        words[0] = words[0].title()
        return ' '.join(words) + '.'
