
from django import forms

from djangoool.models import ISOLanguage

class BasicLanguageSelectField(forms.ModelChoiceField):
	"""A select field for choosing a single basic language."""

	def __init__(self, *args, **kwargs):
		"""Create the field using a basic languages queryset."""
		kwargs['queryset'] = ISOLanguage.objects.basic()
		super(BasicLanguageSelectField, self).__init__(*args, **kwargs)

	def label_from_instance(self, language):
		"""Show a simplified name for each language."""
		return language.simple_name

class BasicLanguagesSelectField(forms.ModelMultipleChoiceField):
	"""A select field for choosing multiple basic languages."""

	def __init__(self, *args, **kwargs):
		"""Create the field using a basic languages queryset."""
		kwargs['queryset'] = ISOLanguage.objects.basic()
		super(BasicLanguagesSelectField, self).__init__(*args, **kwargs)

	def label_from_instance(self, language):
		"""Show a simplified name for each language."""
		return language.simple_name
