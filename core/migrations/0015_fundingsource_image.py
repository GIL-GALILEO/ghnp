# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20170719_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundingsource',
            name='image',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
