from setuptools import find_packages
from setuptools import setup


with open('requirements.txt') as fobj:
    install_requires = [line.strip() for line in fobj]


with open('README.rst') as fobj:
    long_description = fobj.read()


packages = find_packages(exclude=['tests*'])
scripts = ['runserver.py']


setup(
    name='gutenberg_http',
    version='0.0.1',
    author='Clemens Wolff',
    author_email='clemens.wolff+pypi@gmail.com',
    packages=packages,
    url='https://github.com/c-w/gutenberg-http',
    license='LICENSE.txt',
    description='HTTP API for Project Gutenberg',
    long_description=long_description,
    include_package_data=True,
    scripts=scripts,
    install_requires=install_requires)
