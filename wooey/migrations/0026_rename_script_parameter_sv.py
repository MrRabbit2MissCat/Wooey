# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 14:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wooey", "0025_remove_script_parameter_sv"),
    ]

    operations = [
        migrations.RenameField(
            model_name="scriptparameter",
            old_name="script_versions",
            new_name="script_version",
        ),
    ]
