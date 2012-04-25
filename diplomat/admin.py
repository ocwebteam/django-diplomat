
from django.contrib import admin

from diplomat.models import ISOCountry, ISOLanguage

class ISOCountryAdmin(admin.ModelAdmin):
	list_display  = ('alpha2', 'alpha3', 'numeric', 'name', 'official_name')
	ordering      = ('name',)
	search_fields = ('name', 'official_name')

class ISOLanguageAdmin(admin.ModelAdmin):
	list_display  = ('alpha2', 'bibliographic', 'terminology',  'name')
	ordering      = ('name',)
	search_fields = ('name',)

admin.site.register(ISOCountry, ISOCountryAdmin)
admin.site.register(ISOLanguage, ISOLanguageAdmin)
