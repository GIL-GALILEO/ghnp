# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_newspapertype_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundingsource',
            name='name',
        ),
        migrations.AddField(
            model_name='fundingsource',
            name='message',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
