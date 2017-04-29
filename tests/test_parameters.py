from unittest import TestCase

from sanic.exceptions import InvalidUsage

from gutenberg_http import parameters


class ParseFieldsTests(TestCase):
    def test_empty_uses_default(self):
        fields = parameters.parse_fields('')
        self.assertEqual(fields, parameters.ALL_FIELDS)

    def test_parses_valid_fields(self):
        fields = parameters.parse_fields('title,author')
        self.assertEqual(fields, {'title', 'author'})

    def test_bad_field_is_invalid(self):
        with self.assertRaises(InvalidUsage):
            parameters.parse_fields('title,foobar,author')


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
        field, value = parameters.parse_search('title%20eq%20Moby%20Dick')
        self.assertEqual(field, 'title')
        self.assertEqual(value, 'Moby Dick')
