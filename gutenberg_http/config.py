from os import getenv

DB_DIR = getenv('GUTENBERG_DATA')

TEST_PAGE_URL = getenv('GUTENBERG_HTTP_TEST_PAGE_URL',
                       'https://justamouse.com/gutenberg-http')
