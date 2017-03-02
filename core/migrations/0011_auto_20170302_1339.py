# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_type_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewspaperType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='title',
            name='types',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='title',
            name='newspaper_types',
            field=models.ManyToManyField(to='core.NewspaperType'),
        ),
    ]
