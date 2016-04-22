# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('plan_surgery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surgery',
            name='remaining_dimensions',
            field=jsonfield.fields.JSONField(default=datetime.datetime(2016, 4, 15, 9, 12, 50, 605100, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
