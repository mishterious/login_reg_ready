# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0002_auto_20180328_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insp', models.CharField(max_length=255)),
                ('quote_by', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_contribution', to='login_reg_app.User')),
                ('users', models.ManyToManyField(related_name='liked', to='login_reg_app.User')),
            ],
        ),
    ]