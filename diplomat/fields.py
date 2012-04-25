
from django import forms

from diplomat.models import ISOCountry, ISOLanguage

class _CustomChoiceField(object):
	"""Base class for a custom choice field that can provide a default queryset."""

	def __init__(self, *args, **kwargs):
		kwargs['queryset'] = self.provide_queryset()
		super(_CustomChoiceField, self).__init__(*args, **kwargs)

	def provide_queryset(self):
		"""Allow a child field to override the default queryset of the choice field."""
		raise NotImplementedError

class _LanguageField(_CustomChoiceField):
	"""Base class for any field for selecting a language."""

	def label_from_instance(self, language):
		"""Display the language's simple name."""
		return language.simple_name

class LanguageChoiceField(_LanguageField, forms.ModelChoiceField):
	"""A field for choosing a single language."""
	def provide_queryset(self):
		return ISOLanguage.objects.usable()

class LanguageMultipleChoiceField(_LanguageField, forms.ModelMultipleChoiceField):
	"""A field for choosing multiple languages."""
	def provide_queryset(self):
		return ISOLanguage.objects.usable()

class BasicLanguageChoiceField(_LanguageField, forms.ModelChoiceField):
	"""A select field for choosing a single basic language."""
	def provide_queryset(self):
		return ISOLanguage.objects.basic()

class BasicLanguageMultipleChoiceField(_LanguageField, forms.ModelMultipleChoiceField):
	"""A select field for choosing multiple basic languages."""
	def provide_queryset(self):
		return ISOLanguage.objects.basic()

class CountryChoiceField(_CustomChoiceField, forms.ModelChoiceField):
	"""A field for choosing a single country."""
	def provide_queryset(self):
		return ISOCountry.objects.all()

class CountryMultipleChoiceField(_CustomChoiceField, forms.ModelMultipleChoiceField):
	"""A field for choosing multiple countries."""
	def provide_queryset(self):
		return ISOCountry.objects.all()
