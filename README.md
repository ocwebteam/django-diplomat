Djangoool
=========

A Django interface to the pycountry module.  For the moment, only the ISO 639
languages and ISO 3166 countries are included.

Installation
------------

Add `djangoool` to your `INSTALLED_APPS`, then run the `syncdb` management command.
This will create Django databases containing the information from the pycountry
module.

Usage
-----

Djangoool provides Django models that act as wrappers around the objects provided
by pycountry.  Each Django model has attributes that are identical to those of
the pycountry object being mapped to.  The mappings are as follows:

    pycountry.db.Country  => djangoool.models.ISOCountry
    pycountry.db.Language => djangoool.models.ISOLanguage

There are managers on these models and utility fields to make working with them
easier.  You can consult the source to see what these are and how to use them.
