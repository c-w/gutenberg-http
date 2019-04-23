#!/usr/bin/env python3
from multiprocessing import cpu_count
from os import execv
from os import getenv
from os import kill
from os import makedirs
from os import remove
from os.path import dirname
from os.path import join
from signal import SIGHUP
from sys import executable
from tempfile import gettempdir

import click
from jinja2 import Environment
from jinja2 import FileSystemLoader


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
@click.option('--port', default=8080, type=int, envvar='PORT')
@click.option('--host', default='127.0.0.1', envvar='HOST')
@click.option('--workers', default=cpu_count(), type=int, envvar='WORKERS')
@click.option('--gunicorn', default=join(dirname(executable), 'gunicorn'))
@click.option('--config-root', default=join(gettempdir(), 'gutenberg_http'))
def runserver(port, host, workers, gunicorn, config_root):
    makedirs(config_root, exist_ok=True)
    pid_file = join(config_root, 'gunicorn.pid')
    config_file = join(config_root, 'config.py')

    try:
        with open(pid_file, 'rb') as fobj:
            pid = int(fobj.read())
    except (FileNotFoundError, ValueError):
        pid = None

    with open(config_file, 'w', encoding='utf-8') as fobj:
        jinja = Environment(loader=FileSystemLoader(dirname(__file__)))
        jinja.filters['getenv'] = getenv
        fobj.write(jinja.get_template('gunicorn.py.j2').render(**locals()))

    if pid:
        try:
            click.echo('Reloading gunicorn at pid {}'.format(pid))
            kill(pid, SIGHUP)
        except ProcessLookupError:
            remove(pid_file)
            pid = None

    if not pid:
        click.echo('Starting gunicorn with config {}'.format(config_file))

        execv(gunicorn, [
            gunicorn,
            '--config={}'.format(config_file),
            'gutenberg_http:app'
        ])


if __name__ == '__main__':
    cli()
