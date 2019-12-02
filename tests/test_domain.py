from unittest import TestCase

from factory import Faker

from app.domain import Paragraph


class ParagraphTest(TestCase):
    def setUp(self) -> None:
        self.fake_sentence = Faker('sentence')

    def test_can_initialize_with_passing_one_line_string(self) -> None:
        payload = self.fake_sentence.generate()
        paragraph = Paragraph(payload)
        self.assertEqual(payload, paragraph.content)
