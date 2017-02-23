# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20170215_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='slug',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
