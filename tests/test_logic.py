from unittest import TestCase
from unittest.mock import patch

from gutenberg_http import logic


class MetadataTests(TestCase):
    @patch.object(logic, 'get_metadata')
    def test_loads_all_metadata(self, mock_get_metadata):
        self.given_metadatas(mock_get_metadata,
                             ('title', 1, {'Moby Dick'}),
                             ('author', 1, {'Herman, Melville'}),
                             ('title', 2, {'The Jungle Book'}))

        metadata = logic.metadata(fields='', text_id=1)

        self.assertEqual(metadata.pop('title'), {'Moby Dick'})
        self.assertEqual(metadata.pop('author'), {'Herman, Melville'})

    @patch.object(logic, 'get_metadata')
    def test_loads_specific_metadata(self, mock_get_metadata):
        self.given_metadatas(mock_get_metadata,
                             ('title', 1, {'Moby Dick'}),
                             ('author', 1, {'Herman, Melville'}),
                             ('title', 2, {'The Jungle Book'}))

        metadata = logic.metadata(fields='title', text_id=1)

        self.assertEqual(metadata, {'title': {'Moby Dick'}})

    @classmethod
    def given_metadatas(cls, mock_get_metadata, *key_values):
        def side_effect(key, value):
            return next((result for k, v, result in key_values
                         if k == key and v == value), None)

        mock_get_metadata.side_effect = side_effect


class BodyTests(TestCase):
    @patch.object(logic, 'load_etext')
    def test_body(self, mock_load_etext):
        mock_load_etext.return_value = 'some text'

        text = logic.body(123)

        self.assertTrue(text)


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
