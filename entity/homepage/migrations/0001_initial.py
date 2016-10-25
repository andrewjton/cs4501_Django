# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('authenticator', models.CharField(serialize=False, max_length=254, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=600)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('location', models.CharField(max_length=200)),
                ('taken', models.BooleanField()),
                ('date_created', models.DateTimeField(verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateTimeField(verbose_name='birthdate')),
                ('date_created', models.DateTimeField(verbose_name='date created')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='cleaner',
            field=models.ForeignKey(to='homepage.User', null=True, related_name='cleaner_job'),
        ),
        migrations.AddField(
            model_name='job',
            name='owner',
            field=models.ForeignKey(to='homepage.User'),
        ),
        migrations.AddField(
            model_name='authenticator',
            name='user_id',
            field=models.ForeignKey(to='homepage.User'),
        ),
    ]
