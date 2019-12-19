from unittest import TestCase

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
