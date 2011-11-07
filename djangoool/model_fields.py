
from django.db.models import CharField
from django.template.defaultfilters import slugify
from django.utils.encoding import force_unicode

def _get_field(instance, name):
	"""
	Get the attribute named `name` on the model instance `instance` and error
	out if it doesn't exist.
	"""
	try:
		return getattr(instance, name)
	except AttributeError:
		raise ValueError("Model %s has no field '%s'" % \
							 (instance.__class__.__name__, name))

#-------------------------------------------------------------------------------
#  Model Fields
#-------------------------------------------------------------------------------

#  Based on code from http://www.djangosnippets.org/snippets/490/
class AutoSlugField(CharField):
	"""

	A SlugField that automatically populate itself using the value of another
	field.

	In addition to CharField's usual parameters you can specify:

	populate_from (mandatory): the name of the field to be used for the slug
	                           creation. ValueError will be raised at the
	                           object save() time if the field does not exist.

	slugify_func: the function to apply on the value of the field.
	              If unspecified django.template.defaultfilters.slugify will be
	              used.

	append_field: the name of a field that will be appended to the slug, or
	              None. ValueError will be raised at the object save() time if
	              the field does not exist.

	prepend_field: the name of a field that will be prepended to the slug, or
	               None. ValueError will be raised at the object save() time if
	               the field does not exist.

	field_separator: the separator between the slug and the {pre, ap}pended
	                 fields. The default value is u'-'.

	preserve_slug: whether or not to preserve the slug if one is already set.

	Unless explicitly set otherwise, the field will be created with the
	'editable' and 'db_index' parameters set respectively to False and
	True, and 'unique' set to True.

	"""

	def __init__(self, *args, **kwargs):

		if 'editable' not in kwargs:
			kwargs['editable'] = False
		if 'db_index' not in kwargs:
			kwargs['db_index'] = True
		if 'unique' not in kwargs:
			kwargs['unique'] = True

		populate_from   = kwargs.pop('populate_from', None)
		slugify_func    = kwargs.pop('slugify_func', slugify)
		append_field    = kwargs.pop('append_field', None)
		prepend_field   = kwargs.pop('prepend_field', None)
		field_separator = kwargs.pop('field_separator', u'-')
		preserve_slug   = kwargs.pop('preserve_slug', False)

		if populate_from is None:
			raise ValueError("missing 'populate_from' argument")
		else:
			self._populate_from = populate_from

		self._slugify_func    = slugify_func
		self._prepend_field   = prepend_field
		self._append_field    = append_field
		self._field_separator = field_separator
		self._preserve_slug   = preserve_slug

		super(AutoSlugField, self).__init__(*args, **kwargs)

	def pre_save(self, model_instance, add):

		# If the model already has a slug defined and we're supposed to preserve
		# it, take no action
		if self._preserve_slug:
			slug = getattr(model_instance, self.attname, None)
			if slug:
				return slug

		populate_from = _get_field(model_instance, self._populate_from)
		make_slug     = self._slugify_func

		chunks = [make_slug(populate_from)]

		# Prepend a field's value only if it is not empty
		if self._prepend_field is not None:
			prepend_field = _get_field(model_instance, self._prepend_field)
			if prepend_field:
				chunks.insert(0, force_unicode(prepend_field))

		# Append a field's value only if it is not empty
		if self._append_field is not None:
			append_field = _get_field(model_instance, self._append_field)
			if append_field:
				chunks.append(force_unicode(append_field))

		#  Add a trailing number if the slug must be unique for the table
		value = self._field_separator.join(chunks)
		if self.unique:
			collides    = True
			slug_number = 1
			base_name   = value
			model_class = model_instance.__class__
			while collides:
				try:
					existing_model = model_class.objects.get(**{self.attname: value})
				except model_class.DoesNotExist:
					collides = False
				else:
					if model_instance.id is not None and getattr(model_instance, self.attname) == value:
						collides = False
					else:
						value = self._field_separator.join([base_name, force_unicode(slug_number)])
						slug_number += 1

		setattr(model_instance, self.attname, value)
		return value

	def get_internal_type(self):
		return 'SlugField'
