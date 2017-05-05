**************
Gutenberg-HTTP
**************

.. image:: https://travis-ci.org/c-w/gutenberg-http.svg?branch=master
    :target: https://travis-ci.org/c-w/gutenberg-http


Overview
========

This project is an HTTP wrapper for the `Python Gutenberg API <https://github.com/c-w/gutenberg/>`_.
As such, it lets you search for books, retrieve information about books and get
the text of books via a set of easy-to-use HTTP endpoints. `Demo <https://c-w.github.io/gutenberg-http/>`_.

The API is implemented using the `Sanic <https://github.com/channelcat/sanic>`_
web-framework and deployed to an Azure VM behind a nginx reverse proxy.

Endpoints
=========

Fetch all metadata for a book
-----------------------------

.. sourcecode :: sh

    # fetch all metadata for a book-id
    curl 'https://gutenbergapi.org/texts/2701'

.. sourcecode :: json

    {
      "metadata": {
        "title": ["Moby Dick; Or, The Whale"],
        "rights": ["Public domain in the USA."],
        "author": ["Melville, Herman"],
        "subject": [
          "Mentally ill -- Fiction",
          "Whaling -- Fiction",
          "Ship captains -- Fiction",
          "Sea stories",
          "Whaling ships -- Fiction",
          "Psychological fiction",
          "Ahab, Captain (Fictitious character) -- Fiction",
          "PS",
          "Whales -- Fiction",
          "Adventure stories"
        ],
        "language": ["en"]
      },
      "text_id": 2701
    }

Fetch specific metadata for a book
----------------------------------

.. sourcecode :: sh

    # fetch specific metadata for a book-id
    curl 'https://gutenbergapi.org/texts/2701?include=title,author'

.. sourcecode :: json

    {
      "metadata": {
        "author": ["Melville, Herman"],
        "title": ["Moby Dick; Or, The Whale"]
      },
      "text_id": 2701
    }

Fetch the text of a book
------------------------

.. sourcecode :: sh

    # fetch the text for a book-id
    curl 'https://gutenbergapi.org/texts/2701/body'

.. sourcecode

    {
      "text_id": 2701,
      "body": "MOBY DICK; OR THE WHALE\n\n\nBy Herman Melville ... (about 22,000 more lines) ..."
    }

Simple search for books
-----------------------

.. sourcecode :: sh

    # simple single-predicate query with field expansion
    curl 'https://gutenbergapi.org/search/title eq Moby Dick?include=author,rights,language'

.. sourcecode :: json

    {
      "texts": [
        {
          "author": ["Melville, Herman"],
          "language": ["en"],
          "text_id": 9147,
          "rights": ["Copyrighted. Read the copyright notice inside this book for details."]
        },
        {
          "author": ["Melville, Herman"],
          "language": ["en"],
          "text_id": 15,
          "rights": ["Public domain in the USA."]
        }
      ]
    }

Conjunctive query for books
---------------------------

.. sourcecode :: sh

    # conjunctive query
    curl 'https://gutenbergapi.org/search/author eq "Melville, Herman" and rights eq "Public domain in the USA." and title eq "Moby Dick"'

.. sourcecode :: json

    {"texts": [{"text_id": 15}]}
