
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from djangoool.models import ISOCountry, ISOLanguage

def _force_lower(value):
	"""Force a string to be lowercase.

	:param value: arbitrary text
	:type value: str or unicode

	"""
	try:
		return value.lower()
	except AttributeError:
		return None

# Country attributes and filters
COUNTRY_ATTRIBUTES  = ['alpha2', 'alpha3', 'numeric', 'name', 'official_name']
COUNTRY_FILTERS = {
	'alpha2': [_force_lower],
	'alpha3': [_force_lower]}

# Language attributes and filters
LANGUAGE_ATTRIBUTES = ['alpha2', 'bibliographic', 'terminology', 'name']
LANGUAGE_FILTERS = {
	'alpha2': [_force_lower],
	'bibliographic': [_force_lower],
	'terminology': [_force_lower]}

class Command(BaseCommand):

	help = _("creates a database containing the pycountry information")

	def _mirror_pycountry_database(self, source, model, attrs, filters={}):
		"""Create a Django mirror of a pycountry database.

		:param source: a list of pycountry data (countries, languages, etc.)
		:type source: iterable
		:param model: a djangoool model class in which to store the mirrored data
		:type model: class
		:param attrs: the attributes on the pycountry object to mirror
		:type attrs: iterable of strings
		:param filters: an optional dict mapping attributes names to an iterable
		                of functions that should process the value
		:type lower: dict

		"""
		for resource in source:
			mirror = model()
			for attr in attrs:
				value = getattr(resource, attr, None)
				if attr in filters:
					for filter in filters[attr]:
						value = filter(value)
				setattr(mirror, attr, value)
			mirror.save()

	def handle(self, *args, **kwargs):
		"""Create a Django database mirroring the pycountry database."""

		try:
			import pycountry
		except ImportError:
			raise CommandError(_("You must have pycountry installed for djangoool to function properly."))

		# Mirror pycountry's country database
		print _("Syncing pycountry's country list ...")
		ISOCountry.objects.all().delete()
		self._mirror_pycountry_database(pycountry.countries, ISOCountry, COUNTRY_ATTRIBUTES, COUNTRY_FILTERS)

		# Mirror pycountry's language database
		print _("Syncing pycountry's language list ...")
		ISOLanguage.objects.all().delete()
		self._mirror_pycountry_database(pycountry.languages, ISOLanguage, LANGUAGE_ATTRIBUTES, LANGUAGE_FILTERS)
