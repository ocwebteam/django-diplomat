
from django.test import TestCase
import pycountry

from diplomat.models import ISOCountry, ISOLanguage

class ISOCountryTest(TestCase):
	"""Tests for the ISOCountry model."""

	def test_sync(self):
		"""The ISOCountry instances should exactly match the pycountry countries."""
		ISOCountry.pycountry.sync()
		for country in pycountry.countries:
			isocountry = ISOCountry.objects.get(alpha2=country.alpha2)
			for attr in ['alpha2', 'alpha3', 'numeric', 'name', 'official_name']:
				if hasattr(country, attr):
					self.assertEqual(getattr(country, attr), getattr(isocountry, attr))

class ISOLanguageTest(TestCase):
	"""Tests for the ISOLanguage model."""

	def test_sync(self):
		"""The ISOCLanguage instances should exactly match the pycountry languages."""
		ISOLanguage.pycountry.sync()
		for language in pycountry.languages:
			isolanguage = ISOLanguage.objects.get(terminology=language.terminology)
			for attr in ['alpha2', 'bibliographic', 'terminology', 'name']:
				if hasattr(language, attr):
					self.assertEqual(getattr(language, attr), getattr(isolanguage, attr))

	def test_basic_languages(self):
		"""A queryset of basic languages covered by the ISO 639-1 standard should be obtainable."""
		self.assertFalse(ISOLanguage.objects.basic().filter(alpha2__isnull=True).count())

	def test_usable_languages(self):
		"""A queryset of all usable languages covered by the ISO 639-2 standard should be obtainable."""
		non_language_codes = ['mis', 'mul', 'qaa', 'und', 'zxx']
		usable_languages = ISOLanguage.objects.usable()
		for code in non_language_codes:
			self.assertFalse(usable_languages.filter(terminology__startswith=code).count())

	def test_queryset_lengths(self):
		"""The queryset size order, from largest to smallest, is all, usable, basic."""
		self.assertGreater(ISOLanguage.objects.all().count(), ISOLanguage.objects.usable().count())
		self.assertGreater(ISOLanguage.objects.usable().count(), ISOLanguage.objects.basic().count())

	def test_simple_name(self):
		"""The simple name of a language should omit any alternative spellings or date ranges."""
		old_english = ISOLanguage.objects.get(terminology='ang')
		adyghe = ISOLanguage.objects.get(terminology='ady')
		self.assertEqual('English, Old', old_english.simple_name)
		self.assertEqual('Adyghe', adyghe.simple_name)
