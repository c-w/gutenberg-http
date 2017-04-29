from unittest import TestCase
from unittest.mock import patch

from gutenberg_http import logic


class MetadataTests(TestCase):
    pass


class BodyTests(TestCase):
    pass


class SearchTests(TestCase):
    @patch.object(logic, 'get_etexts')
    def test_conjunctive_query(self, mock_get_etexts):
        self.given_texts(mock_get_etexts,
                         ('language', 'en', {1, 2, 3}),
                         ('author', 'Kipling, Rudyard', {2, 3, 4}))

        result = logic.search('language eq en and author eq Kipling, Rudyard')

        self.assertEqual(result, {2, 3})

    @classmethod
    def given_texts(cls, mock_get_etexts, *key_values):
        def side_effect(key, value):
            return next((result for k, v, result in key_values
                         if k == key and v == value), None)

        mock_get_etexts.side_effect = side_effect
