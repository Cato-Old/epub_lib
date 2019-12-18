from unittest import TestCase
from unittest.mock import patch

from app.main import main
from app.settings import Settings


@patch('app.main.sys.argv', ['name', 'path_name'])
@patch('app.main.Book')
class MainTest(TestCase):
    def test_reads_passed_arguments(self, mock_book) -> None:
        main()
        mock_book.assert_called_with('path_name')

    def test_calls_proper_method_on_book(self, mock_book) -> None:
        main()
        mock_book.return_value.dump.assert_called_once()

    @patch('app.main.os.path.abspath', return_value='foo/bar/baz')
    def test_initiates_settings_singleton(self, mock_book, mock_os) -> None:
        main()
        self.assertEqual(Settings().base_path, 'foo/bar/baz')
