
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from diplomat.models import ISOCountry, ISOLanguage

class Command(BaseCommand):

	help = _("creates and populates language and country models")

	def handle(self, *args, **kwargs):
		"""Create a Django database mirroring the pycountry database."""

		print _("Creating country list...")
		ISOCountry.pycountry.sync()

		print _("Creating language list...")
		ISOLanguage.pycountry.sync()
