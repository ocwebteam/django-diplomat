
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField

class ISOCountryManager(models.Manager):
	"""Custom manager for the ISOCountry model."""

	def alphabetical(self):
		"""Return a queryset of countries sorted by their name."""
		return self.order_by('name')

class ISOCountry(models.Model):
	"""A country covered by the ISO 3166-1 standard."""

	objects = ISOCountryManager()

	alpha2  	  = models.CharField(max_length=2, verbose_name=_("alpha-2 code"))
	alpha3  	  = models.CharField(max_length=3, verbose_name=_("alpha-3 code"))
	numeric 	  = models.CharField(max_length=3, verbose_name=_("numeric code"))
	name          = models.CharField(max_length=75, verbose_name=_("name"))
	slug          = AutoSlugField(max_length=75, verbose_name=_("slug"), populate_from="name")
	official_name = models.CharField(max_length=75, verbose_name=_("official name"), null=True, blank=True)

	class Meta:
		verbose_name = _("ISO 3166 country")
		verbose_name_plural = _("ISO 3166 countries")

	def __unicode__(self):
		return self.name

class ISOLanguageManager(models.Manager):
	"""Custom manager for the ISOLanguage model."""

	def basic(self):
		"""Return a queryset of languages covered by the ISO 639-1 standard."""
		return self.filter(alpha2__isnull=False).order_by('name')

	def alphabetical(self):
		"""Return a queryset of all the languages sorted by their reference name."""
		return self.order_by('name')

class ISOLanguage(models.Model):
	"""A language covered by the ISO 639-2 standard."""

	objects = ISOLanguageManager()

	alpha2        = models.CharField(max_length=2, verbose_name=_("ISO 639-1 identifier"), null=True, blank=True)
	bibliographic = models.CharField(max_length=7, verbose_name=_("ISO 639-2 bibliographic identifier"))
	terminology   = models.CharField(max_length=7, verbose_name=_("ISO 639-2 terminology identifier"))
	name          = models.CharField(max_length=100, verbose_name=_("name"))
	slug          = AutoSlugField(max_length=100, verbose_name=_("name slug"), populate_from="name")

	class Meta:
		verbose_name = _("ISO 639 language")
		verbose_name_plural = _("ISO 639 languages")

	def __unicode__(self):
		return self.name

	@property
	def simple_name(self):
		"""Provide a simple name for the language.

		This returns a form of the language name that removes any alternate
		spellings, variants or date ranges provided by pycountry.
		"""
		return re.split(r'[;,\(]', self.name)[0]
