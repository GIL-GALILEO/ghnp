# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_title_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='funding_source',
            field=models.ForeignKey(to='core.FundingSource', null=True),
        ),
    ]
