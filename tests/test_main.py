from unittest import TestCase
from unittest.mock import patch

from app.main import main


@patch('app.main.sys.argv', ['name', 'path_name'])
@patch('app.main.Book')
class MainTest(TestCase):
    def test_reads_passed_arguments(self, mock_book) -> None:
        main()
        mock_book.assert_called_with('path_name')

    def test_calls_proper_method_on_book(self, mock_book) -> None:
        main()
        mock_book.return_value.dump.assert_called_once()
