
import re

from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import ugettext_lazy as _
import pycountry

class PycountryManager(models.Manager):
	"""Base manager for any model that shadows a pycountry database."""

	def sync(self):
		""""Syncs the managed model with its pycountry equivalent."""

		model_fields = self.model._meta.get_all_field_names()

		# Clear all existing model instances
		self.all().delete()

		# Create a new model instance for every datum in the pycountry database
		for resource in self.provide_pycountry_database():
			kwargs = {}
			for field_name in model_fields:
				if hasattr(resource, field_name):
					kwargs[field_name] = getattr(resource, field_name)
			self.create(**kwargs)

	def provide_pycountry_database(self):
		"""Provide the pycountry database that the model shadows."""
		raise NotImplementedError

class ISOCountryManager(models.Manager):
	"""Custom manager for the ISOCountry model."""

	def get_by_natural_key(self, alpha3):
		return self.get(alpha3=alpha3)

class ISOCountryPycountryManager(PycountryManager):
	"""Pycountry manager for the ISOCountry model."""

	def provide_pycountry_database(self):
		return pycountry.countries

class ISOCountry(models.Model):
	"""A country covered by the ISO 3166-1 standard."""

	objects   = ISOCountryManager()
	pycountry = ISOCountryPycountryManager()

	alpha2  	  = models.CharField(max_length=2, verbose_name=_("alpha-2 code"), unique=True)
	alpha3  	  = models.CharField(max_length=3, verbose_name=_("alpha-3 code"), unique=True)
	numeric 	  = models.CharField(max_length=3, verbose_name=_("numeric code"))
	name          = models.CharField(max_length=75, verbose_name=_("name"), unique=True)
	slug          = AutoSlugField(max_length=75, verbose_name=_("slug"), populate_from="name", unique=True)
	official_name = models.CharField(max_length=75, verbose_name=_("official name"), null=True, blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _("ISO 3166 country")
		verbose_name_plural = _("ISO 3166 countries")

	def __unicode__(self):
		return self.name

	def natural_key(self):
		return (self.alpha3,)

class ISOLanguageManager(models.Manager):
	"""Custom manager for the ISOLanguage model."""

	# The special non-language ISO 639-2 codes
	_NON_LANGUAGES_CODES = ('mis', 'mul', 'qaa-qtz', 'und', 'zxx')

	def basic(self):
		"""Return a queryset of languages covered by the ISO 639-1 standard."""
		return self.filter(alpha2__isnull=False)

	def usable(self):
		"""The full list of usable ISO 639-2 human languages.

		This is effectively a list of all languages with the special ISO 639-2
		non-language codes excluded.
		"""
		return self.all().exclude(terminology__in=self._NON_LANGUAGES_CODES)

	def get_by_natural_key(self, terminology):
		return self.get(terminology=terminology)

class ISOLanguagePycountryManager(PycountryManager):
	"""Pycountry manager for the ISOLanguage model."""

	def provide_pycountry_database(self):
		return pycountry.languages

class ISOLanguage(models.Model):
	"""A language covered by the ISO 639-2 standard."""

	objects   = ISOLanguageManager()
	pycountry = ISOLanguagePycountryManager()

	alpha2        = models.CharField(max_length=2, verbose_name=_("ISO 639-1 identifier"), null=True, blank=True)
	bibliographic = models.CharField(max_length=7, verbose_name=_("ISO 639-2 bibliographic identifier"), unique=True)
	terminology   = models.CharField(max_length=7, verbose_name=_("ISO 639-2 terminology identifier"), unique=True)
	name          = models.CharField(max_length=100, verbose_name=_("name"), unique=True)
	slug          = AutoSlugField(max_length=100, verbose_name=_("name slug"), populate_from="name", unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _("ISO 639 language")
		verbose_name_plural = _("ISO 639 languages")

	def __unicode__(self):
		return self.name

	def natural_key(self):
		return (self.terminology,)

	@property
	def simple_name(self):
		"""The language name stripped of variant spellings and date ranges."""
		return re.split(r'[;\(]', self.name)[0].strip()
