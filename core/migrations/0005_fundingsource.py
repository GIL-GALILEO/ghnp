# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170106_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
    ]
