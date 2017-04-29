from unittest import TestCase

from gutenberg_http.cache import lru_cache_truthy_only


class LruCacheTruthyOnlyTests(TestCase):
    def setUp(self):
        self.method_call_count = 0

        @lru_cache_truthy_only(maxsize=8)
        def some_method(num: int):
            self.method_call_count += 1
            return num * 2 if num else 0

        self.some_method = some_method

    def test_caches_truthy_value(self):
        self.assertTrue(self.some_method(123))
        self.assertTrue(self.some_method(123))
        self.assertEqual(self.method_call_count, 1)

        self.assertTrue(self.some_method(456))
        self.assertEqual(self.method_call_count, 2)

    # noinspection PyTypeChecker
    def test_does_not_cache_falsy_value(self):
        self.assertEqual(self.some_method(0), 0)
        self.assertEqual(self.some_method(0), 0)
        self.assertEqual(self.method_call_count, 2)

    def test_exposes_cache_statistics(self):
        self.some_method(123)
        self.some_method(123)
        self.some_method(123)
        self.some_method(456)
        self.some_method(0)
        self.some_method(0)
        self.some_method(0)

        cache_info = self.some_method.cache_info()
        self.assertEqual(cache_info.hits, 2)
        self.assertEqual(cache_info.currsize, 2)
