#!/usr/bin/env python3
from multiprocessing import cpu_count
from os import execvp
from pathlib import Path
from sys import executable

import click

HOSTS = ('127.0.0.1', '0.0.0.0')


@click.group(chain=True)
def cli():
    pass


@cli.command('initdb')
def initdb():
    from gutenberg.acquire import get_metadata_cache

    cache = get_metadata_cache()
    click.echo('Using database at {}'.format(cache.cache_uri))

    if not cache.exists:
        click.echo('Setting up database... this may take a while')
        cache.populate()


@cli.command('runserver')
@click.option('--port', default=8080, type=int)
@click.option('--host', default=HOSTS[0], type=click.Choice(HOSTS))
@click.option('--workers', default=cpu_count(), type=int)
@click.option('--gunicorn', default=str(Path(executable).parent / 'gunicorn'))
def runserver(port, host, workers, gunicorn):
    click.echo('Starting {} workers on {}:{}'.format(workers, host, port))

    execvp(gunicorn, [
        gunicorn,
        '--bind={}:{}'.format(host, port),
        '--workers={}'.format(workers),
        '--worker-class=sanic.worker.GunicornWorker',
        'gutenberg_http:app'
    ])


if __name__ == '__main__':
    cli(auto_envvar_prefix='GUTENBERG_HTTP')
