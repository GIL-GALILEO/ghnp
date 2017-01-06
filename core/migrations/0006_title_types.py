# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_fundingsource'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='types',
            field=models.ManyToManyField(to='core.Type'),
        ),
    ]
