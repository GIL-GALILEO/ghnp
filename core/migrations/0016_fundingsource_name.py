# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_fundingsource_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundingsource',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
