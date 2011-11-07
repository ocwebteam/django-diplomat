
from django.core.management import call_command
from django.db.models import signals

import djangoool.models as djangoool_app
from djangoool.models import ISOCountry, ISOLanguage

def sync_pycountry(app, created_models, verbosity, **kwargs):
	"""
	Populate the pycountry Django tables after the database has been synced, if the
	tables has yet to be populated.
	"""
	if ISOLanguage in created_models or ISOCountry in created_models:
		call_command("syncdjangoool")

signals.post_syncdb.connect(sync_pycountry,
	sender=djangoool_app, dispatch_uid="djangoool.management.sync_pycountry")
