# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170302_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='essay',
            name='titles',
        ),
        migrations.AddField(
            model_name='title',
            name='essay_text',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='Essay',
        ),
    ]
