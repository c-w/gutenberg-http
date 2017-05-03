#!/usr/bin/env python3
from argparse import ArgumentParser
from multiprocessing import cpu_count
from sys import stderr

from gutenberg.acquire import get_metadata_cache

from gutenberg_http import app

HOSTS = ('127.0.0.1', '0.0.0.0')

parser = ArgumentParser(__doc__)
parser.add_argument('--port', type=int, default=8080)
parser.add_argument('--host', choices=HOSTS, default=HOSTS[0])
parser.add_argument('--workers', type=int, default=cpu_count())
args = parser.parse_args()

cache = get_metadata_cache()
if not cache.exists:
    print('Setting up Gutenberg... this may take a while', file=stderr)
    cache.populate()

app.run(host=args.host, port=args.port, workers=args.workers)
