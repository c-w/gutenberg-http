from unittest import TestCase
from unittest.mock import patch

from gutenberg_http import logic


def _setup_mock_query(mock, *key_values):
    def side_effect(key, value):
        return next((result for k, v, result in key_values
                     if k == key and v == value), None)

    mock.side_effect = side_effect


class MetadataTests(TestCase):
    @patch.object(logic, 'get_metadata')
    def test_loads_all_metadata(self, mock_get_metadata):
        _setup_mock_query(mock_get_metadata,
                          ('title', 1, {'Moby Dick'}),
                          ('author', 1, {'Herman, Melville'}),
                          ('title', 2, {'The Jungle Book'}))

        metadata = logic.metadata(text_id=1)

        self.assertEqual(metadata.pop('title'), {'Moby Dick'})
        self.assertEqual(metadata.pop('author'), {'Herman, Melville'})

    @patch.object(logic, 'get_metadata')
    def test_loads_specific_metadata(self, mock_get_metadata):
        _setup_mock_query(mock_get_metadata,
                          ('title', 1, {'Moby Dick'}),
                          ('author', 1, {'Herman, Melville'}),
                          ('title', 2, {'The Jungle Book'}))

        metadata = logic.metadata(text_id=1, include='title')

        self.assertEqual(metadata, {'title': {'Moby Dick'}})


class BodyTests(TestCase):
    @patch.object(logic, 'load_etext')
    def test_body(self, mock_load_etext):
        mock_load_etext.return_value = 'some text'

        text = logic.body(123)

        self.assertTrue(text)


class SearchTests(TestCase):
    @patch.object(logic, 'get_etexts')
    def test_conjunctive_query(self, mock_get_etexts):
        _setup_mock_query(mock_get_etexts,
                          ('language', 'en', {1, 2, 3}),
                          ('author', 'Kipling, Rudyard', {2, 3, 4}))

        result = logic.search('language eq en and author eq Kipling, Rudyard')

        self.assertEqual(result, [{'text_id': 2}, {'text_id': 3}])

    @patch.object(logic, 'get_etexts')
    @patch.object(logic, 'get_metadata')
    def test_query_expands_fields(self, mock_get_metadata, mock_get_etexts):
        _setup_mock_query(mock_get_etexts,
                          ('author', 'Kipling, Rudyard', {2}))
        _setup_mock_query(mock_get_metadata,
                          ('title', 2, {'The Jungle Book'}),
                          ('author', 2, {'Kipling, Rudyard'}))

        result = logic.search('author eq Kipling, Rudyard', 'title,author')

        self.assertEqual(result, [{
            'text_id': 2,
            'title': {'The Jungle Book'},
            'author': {'Kipling, Rudyard'},
        }])
