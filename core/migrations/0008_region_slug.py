# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_title_funding_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='slug',
            field=models.CharField(max_length=50),
        ),
    ]
