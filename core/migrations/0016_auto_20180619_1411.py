# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_issue_api_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='api_available',
        ),
        migrations.AddField(
            model_name='batch',
            name='api_available',
            field=models.BooleanField(default=True),
        ),
    ]
