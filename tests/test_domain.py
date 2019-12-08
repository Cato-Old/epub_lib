from importlib import import_module
from typing import Type
from unittest import TestCase

from factory import Faker

from app.domain import Paragraph, ParagraphType, Page


def get_faker_with_provider(locale: str = None) -> Type[Faker]:
    locale = locale if locale else 'en_US'
    base_provider = import_module(f'faker.providers.lorem.{locale}')

    class Provider(base_provider.Provider):
        def text_with_newline(self, par_num=2):
            par = self.paragraph
            return '\n'.join(f'{par()}' for _ in range(par_num+1))

        def marked_text_with_newline(self, prefixes) -> str:
            par = self.paragraph
            return '\n'.join(f'{prefix}{par()}' for prefix in prefixes)

        def page(self, num=None):
            mark = f'Str{num or self.random_int(1, 500)}'
            content = self.marked_text_with_newline(['', '$>', '$>'])
            return '\n'.join((mark, content))

    faker = Faker
    faker.add_provider(Provider)
    return faker


class ParagraphTest(TestCase):
    def setUp(self) -> None:
        self.faker = get_faker_with_provider()
        self.paragraph_test_params = [
            (
                ParagraphType.CONTINUATION,
                self.faker('sentence').generate(),
                '<p>.+</p>'
            ),
            (
                ParagraphType.INDENT,
                f'$>{self.faker("sentence").generate()}',
                '<p class="a2">.+</p>'
            ),
        ]

    def test_can_initialize_with_passing_oneline_string(self) -> None:
        payload = self.faker('sentence').generate()
        paragraph = Paragraph(payload)
        self.assertEqual(payload, paragraph.content)

    def test_raises_when_initialized_with_multiline_string(self):
        with self.assertRaises(ValueError):
            Paragraph(self.faker('text_with_newline').generate())

    def test_set_paragraph_type_on_initialization(self):
        for expected_type, content, _ in self.paragraph_test_params:
            with self.subTest(expected_type):
                paragraph = Paragraph(content)
                self.assertIs(paragraph.type, expected_type)

    def test_dumps_to_accurate_string(self):
        for tested_type, content, exp_regex in self.paragraph_test_params:
            with self.subTest(tested_type):
                paragraph = Paragraph(content)
                actual = paragraph.dump()
                self.assertRegex(actual, exp_regex)


class PageTest(TestCase):
    def setUp(self):
        self.faker = get_faker_with_provider()

    def test_set_page_number_on_initialization(self) -> None:
        expected_number = self.faker('random_int', min=1, max=500).generate()
        raw_page = self.faker('page', num=expected_number).generate()
        page = Page(raw_page)
        self.assertEqual(expected_number, page.number)

    def test_raises_when_initialized_with_invalid_page_number(self) -> None:
        exception_msg = r'.+ is not a page number'
        with self.assertRaisesRegex(ValueError, exception_msg):
            Page(self.faker('page', num='not_a_number').generate())

    def test_raises_when_initialized_without_page_number(self) -> None:
        exception_msg = r'.+ is not a page description'
        with self.assertRaisesRegex(ValueError, exception_msg):
            Page(self.faker('text_with_newline').generate())
