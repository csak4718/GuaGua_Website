# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(verbose_name=b'created at')),
                ('updatedAt', models.DateTimeField(verbose_name=b'updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_id', models.CharField(max_length=200)),
                ('numA', models.IntegerField(default=0)),
                ('numB', models.IntegerField(default=0)),
                ('choiceA', models.CharField(max_length=200)),
                ('choiceB', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(verbose_name=b'created at')),
                ('updatedAt', models.DateTimeField(verbose_name=b'updated at')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='question',
            field=models.ForeignKey(to='guagua.Question'),
        ),
    ]
