**************
Gutenberg-HTTP
**************

.. image:: https://travis-ci.org/c-w/gutenberg-http.svg?branch=master
    :target: https://travis-ci.org/c-w/gutenberg-http


Overview
========

This project is a HTTP wrapper for the `Python Gutenberg API <https://github.com/c-w/gutenberg/>`_.
As such, it lets you search for books

Endpoints
=========

Fetch all metadata for a book
-----------------------------

.. sourcecode :: sh

    # fetch all metadata for a book-id
    curl 'http://gutenbergapi.org/texts/2701'

.. sourcecode :: json

    {
      "metadata": {
        "title": [
          "Moby Dick; Or, The Whale"
        ],
        "rights": [
          "Public domain in the USA."
        ],
        "author": [
          "Melville, Herman"
        ],
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
        "language": [
          "en"
        ]
      },
      "text_id": 2701
    }

Fetch specific metadata for a book
----------------------------------

.. sourcecode :: sh

    # fetch specific metadata for a book-id
    curl 'http://gutenbergapi.org/texts/2701?fields=title,author'

.. sourcecode :: json

    {
      "metadata": {
        "author": [
          "Melville, Herman"
        ],
        "title": [
          "Moby Dick; Or, The Whale"
        ]
      },
      "text_id": 2701
    }

Fetch the text of a book
------------------------

.. sourcecode :: sh

    # fetch the text for a book-id
    curl 'http://gutenbergapi.org/texts/2701/body'

.. sourcecode

    MOBY DICK; OR THE WHALE

    By Herman Melville

    ... (about 22,000 more lines) ...


Simple search for books
-----------------------

.. sourcecode :: sh

    # simple single-predicate query
    curl 'http://gutenbergapi.org/search/author eq Melville, Herman'

.. sourcecode :: json

    {"text_ids":[2694,2701,4045,15,13720,13721,34970,10712,11231,12384,23969,53861,28794,12841,1900,28656,15859,9268,9269,8118,21816,2489,9146,9147,15422]}

Complex search for books
------------------------

.. sourcecode :: sh

    # conjunctive query
    curl 'http://gutenbergapi.org/search/author eq "Melville, Herman" and title eq "Moby Dick"'

.. sourcecode :: json

    {"text_ids":[9147,15]}
