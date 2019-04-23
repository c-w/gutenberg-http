#!/usr/bin/env python3
from multiprocessing import cpu_count

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
def runserver(port, host, workers):
    from gutenberg_http import app

    click.echo('Starting {} workers on {}:{}'.format(workers, host, port))
    app.run(host=host, port=port, workers=workers)


if __name__ == '__main__':
    cli(auto_envvar_prefix='GUTENBERG_HTTP')
