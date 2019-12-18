from unittest import TestCase

from app.settings import Settings


class SettingsTest(TestCase):
    def test_can_save_state_globally(self) -> None:
        actual = Settings(path='foo/bar/baz')
        expected = Settings()
        self.assertEqual(actual.path, expected.path)

    def test_cannot_change_initiated_value(self) -> None:
        settings = Settings(path='foo/bar/baz')
        with self.assertRaises(TypeError):
            settings.path = 'bar/baz/foo'

    def tearDown(self) -> None:
        Settings.clear()
