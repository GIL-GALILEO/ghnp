# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170413_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspapertype',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
