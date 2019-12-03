from importlib import import_module
from unittest import TestCase

from factory import Faker

from app.domain import Paragraph


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

    def test_can_initialize_with_passing_oneline_string(self) -> None:
        payload = self.fake_sentence.generate()
        paragraph = Paragraph(payload)
        self.assertEqual(payload, paragraph.content)

    def test_raises_when_initialized_with_multiline_string(self):
        with self.assertRaises(ValueError):
            Paragraph(self.fake_text.generate())
