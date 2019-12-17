import os
from importlib import import_module
from string import Template
from typing import Type
from unittest import TestCase

from factory import Faker

from app.domain import Paragraph, ParagraphType, Page, Book


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

        def page(self, num=None, prefixes=None):
            prefixes = prefixes if prefixes is not None else ['', '$>', '$>']
            mark = f'Str{num or self.random_int(1, 500)}'
            content = self.marked_text_with_newline(prefixes)
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
                '<p>.+</p>',
            ),
            (
                ParagraphType.INDENT,
                f'$>{self.faker("sentence").generate()}',
                '<p class="a2">.+</p>',
            ),
            (
                ParagraphType.CHAPTER_HEADER,
                f'$h2>{self.faker("sentence").generate()}',
                r'<h2>[^\$].+</h2>',
            )
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
        self.expected_number = self.faker(
            'random_int', min=1, max=500
        ).generate()

    def test_set_page_number_on_initialization(self) -> None:
        raw_page = self.faker('page', num=self.expected_number).generate()
        self.assertEqual(self.expected_number, Page(raw_page).number)

    def test_raises_when_initialized_with_invalid_page_number(self) -> None:
        exception_msg = r'.+ is not a page number'
        with self.assertRaisesRegex(ValueError, exception_msg):
            Page(self.faker('page', num='not_a_number').generate())

    def test_raises_when_initialized_without_page_number(self) -> None:
        exception_msg = r'.+ is not a page description'
        with self.assertRaisesRegex(ValueError, exception_msg):
            Page(self.faker('text_with_newline').generate())

    def test_set_paragraphs_on_initialization(self) -> None:
        prefixes_map = {
            '$>': ParagraphType.INDENT,
            '': ParagraphType.CONTINUATION,
        }
        prefixes = ['', '$>', '$>']
        page = Page(self.faker('page', prefixes=prefixes).generate())
        self.assertListEqual(
            [paragraph.type for paragraph in page.paragraphs],
            [prefixes_map[p] for p in prefixes]
        )

    def test_dumps_paragraphs_to_accurate_string(self) -> None:
        prefixes = ['', '$>', '$>']
        page = Page(self.faker('page', prefixes=prefixes).generate())
        expected = r'<p>.+</p>\n<p class="a2">.+</p>\n<p class="a2">.+</p>'
        self.assertRegex(page.dump(), expected)

    def test_dumps_page_to_file(self) -> None:
        prefixes = ['', '$>', '$>']
        page = Page(self.faker(
            'page', num=self.expected_number, prefixes=prefixes
        ).generate())
        content = page.dump()
        with open('../resources/template.xhtml', 'r') as f:
            template = Template(f.read())
        expected = template.substitute(
            page_number=self.expected_number, content=content,
        )
        page.dump_to_file()
        with open(f'{self.expected_number}.xhtml', 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)

    def tearDown(self):
        for file in os.listdir(os.getcwd()):
            if '.xhtml' in file:
                os.remove(file)


class BookTest(TestCase):
    def setUp(self) -> None:
        self.faker = get_faker_with_provider()

    def test_can_be_initialized_from_file(self) -> None:
        page_numbers = [
            self.faker('random_int', min=1, max=500).generate()
            for _ in range(3)
        ]
        book = self._build_book(page_numbers)
        self.assertListEqual(page_numbers, [p.number for p in book.pages])

    def test_dumps_pages_to_files(self) -> None:
        page_numbers = [
            self.faker('random_int', min=1, max=500).generate()
            for _ in range(3)
        ]
        book = self._build_book(page_numbers)
        book.dump()
        self.assertSetEqual(
            {int(f[:-6]) for f in os.listdir(os.getcwd()) if '.xhtml' in f},
            set(page_numbers)
        )

    def _build_book(self, page_numbers: list) -> Book:
        pages = '\n'.join(
            self.faker('page', num=number).generate()
            for number in page_numbers
        )
        with open('pages.txt', 'w') as f:
            f.write(pages)
        return Book('pages.txt')

    def tearDown(self) -> None:
        os.remove('pages.txt')
        for file in os.listdir(os.getcwd()):
            if '.xhtml' in file:
                os.remove(file)
