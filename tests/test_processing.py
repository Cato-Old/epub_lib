from random import randint
from unittest import TestCase

from factory import Faker

from app.domain import ParagraphType
from app.processing import ParagraphProcessor
from tests.test_domain import PARAGRAPH_TEST_PARAMS


class ParagraphProcessorTest(TestCase):
    def setUp(self) -> None:
        self.processor = ParagraphProcessor()
        self.params = PARAGRAPH_TEST_PARAMS

    def test_processes_raw_text_type_marker(self) -> None:
        for tested_type, content, regex_content, _ in self.params:
            with self.subTest(tested_type):
                actual = self.processor.process(content, tested_type)
                self.assertRegex(actual, regex_content)

    def test_processes_raw_text_italic_markers(self) -> None:
        payload = self.sentence_with_italic()
        actual = self.processor.process(payload, ParagraphType.CONTINUATION)
        self.assertRegex(actual, r'.*<i>.+</i>.*')

    def sentence_with_italic(self) -> str:
        words = Faker('words', nb=randint(1, 10)).generate()
        ind = randint(0, len(words)-1)
        words[ind] = f'€{words[ind]}€'
        words[0] = words[0].title()
        return ' '.join(words) + '.'
