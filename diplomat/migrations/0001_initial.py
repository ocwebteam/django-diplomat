# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ISOCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alpha2', models.CharField(unique=True, verbose_name='alpha-2 code', max_length=2)),
                ('alpha3', models.CharField(unique=True, verbose_name='alpha-3 code', max_length=3)),
                ('numeric', models.CharField(verbose_name='numeric code', max_length=3)),
                ('name', models.CharField(unique=True, verbose_name='name', max_length=75)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, max_length=75, verbose_name='slug', populate_from='name', editable=False)),
                ('official_name', models.CharField(null=True, blank=True, verbose_name='official name', max_length=75)),
            ],
            options={
                'verbose_name_plural': 'ISO 3166 countries',
                'ordering': ('name',),
                'verbose_name': 'ISO 3166 country',
            },
        ),
        migrations.CreateModel(
            name='ISOLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alpha2', models.CharField(null=True, blank=True, verbose_name='ISO 639-1 identifier', max_length=2)),
                ('bibliographic', models.CharField(unique=True, verbose_name='ISO 639-2 bibliographic identifier', max_length=7)),
                ('terminology', models.CharField(unique=True, verbose_name='ISO 639-2 terminology identifier', max_length=7)),
                ('name', models.CharField(unique=True, verbose_name='name', max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, max_length=100, verbose_name='name slug', populate_from='name', editable=False)),
            ],
            options={
                'verbose_name_plural': 'ISO 639 languages',
                'ordering': ('name',),
                'verbose_name': 'ISO 639 language',
            },
        ),
    ]
