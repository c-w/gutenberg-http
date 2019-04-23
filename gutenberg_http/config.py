from os import getenv

DB_DIR = getenv('GUTENBERG_DATA')

METADATA_CACHE_SIZE = int(getenv('GUTENBERG_HTTP_METADATA_CACHE_SIZE', '1024'))
BODY_CACHE_SIZE = int(getenv('GUTENBERG_HTTP_BODY_CACHE_SIZE', '64'))
SEARCH_CACHE_SIZE = int(getenv('GUTENBERG_HTTP_SEARCH_CACHE_SIZE', '128'))

TEST_PAGE_URL = getenv('GUTENBERG_HTTP_TEST_PAGE_URL',
                       'https://justamouse.com/gutenberg-http')
