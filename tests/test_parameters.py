from unittest import TestCase

from gutenberg_http import parameters
from gutenberg_http.errors import InvalidUsage


class ParseIncludeTests(TestCase):
    def test_empty_uses_default(self):
        fields = parameters.parse_include('')
        self.assertEqual(fields, parameters.ALL_FIELDS)

    def test_parses_valid_includes(self):
        fields = parameters.parse_include('title,author')
        self.assertEqual(fields, {'title', 'author'})

    def test_bad_include_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_include('title,foobar,author')


class ParseSearchTests(TestCase):
    def test_empty_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_search('')

    def test_bad_operator_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_search('field foobar value')

    def test_bad_field_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_search('foobar eq value')

    def test_no_value_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_search('title eq')

    def test_parses_correct_url_encoded_query(self):
        [(field, value)] = parameters.parse_search('title%20eq%20Moby%20Dick')
        self.assertEqual(field, 'title')
        self.assertEqual(value, 'Moby Dick')

    def test_parses_correct_quoted_query(self):
        [(field, value)] = parameters.parse_search('title eq "Moby Dick"')
        self.assertEqual(field, 'title')
        self.assertEqual(value, 'Moby Dick')

        [(field, value)] = parameters.parse_search("title eq 'Moby Dick'")
        self.assertEqual(field, 'title')
        self.assertEqual(value, 'Moby Dick')

    def test_parses_correct_conjunctive_query(self):
        query = 'title eq Moby Dick and author eq Melville, Herman'
        [(field1, value1), (field2, value2)] = parameters.parse_search(query)
        self.assertEqual(field1, 'title')
        self.assertEqual(value1, 'Moby Dick')
        self.assertEqual(field2, 'author')
        self.assertEqual(value2, 'Melville, Herman')
