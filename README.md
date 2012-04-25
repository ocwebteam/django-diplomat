Diplomat
========

Diplomat provides Django models for the countries and languages covered by the 
ISO 3166 and ISO 639 standards, respectively.  Diplomat is implemented as a 
wrapper around a subset of pycountry, and its interface should feel familiar to 
users of that module.

Installation
============

Add `diplomat` to your `INSTALLED_APPS`, then run the `syncdb` command, which
will create the required language and country models.

Model Usage
===========

Diplomat's field models exactly mirror the attributes of the pycountry database
objects that they imitate.  In addition to these attributes, custom manager
methods are available for some of the objects provided by diplomat.

Languages
---------

The `ISOLanguage` model is a wrapper around the `pycountry.db.Language` model.

    >>> from diplomat.models import ISOLanguage
    >>> aragonese = ISOLanguage.objects.get(alpha2='an')
    >>> aragonese.alpha2
    u'an'
    >>> aragonese.bibliographic
    u'arg'
    >>> aragonese.terminology
    u'arg'
    >>> aragonese.name
    u'Aragonese'

In addition, it provides a custom model manager.

    >>> from diplomat.models import ISOLanguage
    >>> all_languages = ISOLanguage.objects.all()
    >>> basic_languages = ISOLanguage.objects.basic()
    >>> usable_languages = ISOLanguage.objects.usable()
    >>> all_languages.count() > usable_languages.count() > basic_languages.count()
    True
    >>> all([l.alpha2 for l in all_languages])
    False
    >>> all([l.alpha2 for l in basic_languages])
    True
    >>> all_languages.filter(terminology='zxx').count()
    1
    >>> usable_languages.filter(terminology='zxx').count()
    0

Countries
---------

The `ISOCountry` model is a wrapper around the `pycountry.db.Country` model.

    >>> from diplomat.models import ISOCountry
    >>> germany = ISOCountry.objects.get(alpha2='DE')
    >>> germany.alpha2
    u'DE'
    >>> germany.alpha3
    u'DEU'
    >>> germany.numeric
    u'276'
    >>> germany.name
    u'Germany'
    >>> germany.official_name
    u'Federal Republic of Germany'

Field Usage
===========

Diplomat provides a series of simple form fields for selecting country and
language objects.  These fields, which can be imported from `diplomat.fields`,
are as follows:

**LanguageChoiceField**  
A field for selecting a single usable language.

**LanguageMultipleChoiceField**  
A field for selecting multiple usable languages.

**BasicLanguageChoiceField**  
A field for selecting a single basic language covered by ISO 639-1.

**BasicLanguageMultipleChoiceField**  
A field for selecting multiple basic languages covered by ISO 639-1.

**CountryChoiceField**  
A field for selecting a single country.

**CountryMultipleChoiceField**  
A field for selecting multiple countries.
