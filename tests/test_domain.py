from importlib import import_module
from unittest import TestCase

from factory import Faker

from app.domain import Paragraph, ParagraphType


def get_provider(locale: str = None):
    locale = locale if locale else 'en_US'
    base_provider = import_module(f'faker.providers.lorem.{locale}')

    class Provider(base_provider.Provider):
        def text_with_newline(self):
            return f'{self.paragraph()}\n{self.paragraph()}'

    return Provider


class ParagraphTest(TestCase):
    def setUp(self) -> None:
        faker = Faker
        faker.add_provider(get_provider())
        self.fake_sentence = faker('sentence')
        self.fake_text = faker('text_with_newline')
        self.paragraph_test_params = [
            (ParagraphType.CONTINUATION, self.fake_sentence.generate()),
            (ParagraphType.INDENT, f'$>{self.fake_sentence.generate()}'),
        ]

    def test_can_initialize_with_passing_oneline_string(self) -> None:
        payload = self.fake_sentence.generate()
        paragraph = Paragraph(payload)
        self.assertEqual(payload, paragraph.content)

    def test_raises_when_initialized_with_multiline_string(self):
        with self.assertRaises(ValueError):
            Paragraph(self.fake_text.generate())

    def test_set_paragraph_type_on_initialization(self):
        for expected_type, content in self.paragraph_test_params:
            with self.subTest(expected_type):
                paragraph = Paragraph(content)
                self.assertIs(paragraph.type, expected_type)
