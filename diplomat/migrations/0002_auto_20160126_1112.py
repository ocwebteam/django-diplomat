# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplomat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='isocountry',
            options={'verbose_name_plural': 'ISO 3166 countries', 'verbose_name': 'ISO 3166 country', 'ordering': ('-sort_index', 'name')},
        ),
        migrations.AddField(
            model_name='isocountry',
            name='sort_index',
            field=models.IntegerField(default=0),
        ),
    ]
