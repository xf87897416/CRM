# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-02-12 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_contracttemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ContractTemplate'),
        ),
    ]
