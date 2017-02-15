# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_region_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='homepage_copy',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='region',
            name='homepage_image',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fundingsource',
            name='name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fundingsource',
            name='slug',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='slug',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
