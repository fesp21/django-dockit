Introduction
============

django-dockitcms provides a Document ORM in django. Dockitcms attempts to provide a batteries included experience while preserving django's various conventions.

--------
Features
--------

* Mongodb support
* Backend for using django models to store documents (see Django Document)
* Integrates with the django admin
 * Supports inlines
 * List Field support (under progress)
 * Supports editing documents with deeply nested schemas
 * Robust design for customizing behavior on a per schema basis
* Class based views
* Django forms support
* Dynamically typed documents and schemas


Installation
============

------------
Requirements
------------

* Python 2.5 or later
* Django 1.3


--------
Settings
--------

Put 'dockit' into your ``INSTALLED_APPS`` section of your settings file.


Configuring Document Store Backend
----------------------------------

===============
Django Document
===============

Set the following in your settings file::

    DOCKIT_BACKEND = 'dockit.backends.djangodocument.backend.ModelDocumentStorage'


=======
Mongodb
=======

Set the following in your settings file::

    DOCKIT_BACKEND = 'dockit.backends.mongo.backend.MongoDocumentStorage'
    MONGO_HOST = '127.0.0.1
    MONGO_PORT = 27017
    MONGO_USER = ''
    MONGO_PASSWORD = ''
    MONGO_DB = ''

Note: the configuration parameters are likely to change in the future.
