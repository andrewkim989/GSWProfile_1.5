# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-15 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('birth_month', models.CharField(max_length=2)),
                ('birth_day', models.CharField(max_length=2)),
                ('birth_year', models.CharField(max_length=4)),
                ('height_foot', models.CharField(max_length=1)),
                ('height_inches', models.CharField(max_length=2)),
                ('weight', models.CharField(max_length=3)),
                ('position', models.CharField(max_length=15)),
                ('teams_played', models.TextField(max_length=255)),
                ('teams_coached', models.TextField(max_length=255)),
                ('college', models.CharField(max_length=50)),
                ('draft', models.CharField(max_length=50)),
                ('playfrom', models.CharField(max_length=4)),
                ('playto', models.CharField(max_length=4)),
                ('coachfrom', models.CharField(max_length=4)),
                ('coachto', models.CharField(max_length=7)),
                ('coach_position', models.CharField(max_length=30)),
                ('info', models.TextField(max_length=1000)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('birth_month', models.CharField(max_length=2)),
                ('birth_day', models.CharField(max_length=2)),
                ('birth_year', models.CharField(max_length=4)),
                ('height_foot', models.CharField(max_length=1)),
                ('height_inches', models.CharField(max_length=2)),
                ('weight', models.CharField(max_length=3)),
                ('position', models.CharField(max_length=50)),
                ('info', models.TextField(max_length=1000)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('other_comments', models.ManyToManyField(related_name='other_commented', to='gsw.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('birth_month', models.CharField(max_length=2)),
                ('birth_day', models.CharField(max_length=2)),
                ('birth_year', models.CharField(max_length=4)),
                ('height_foot', models.CharField(max_length=1)),
                ('height_inches', models.CharField(max_length=2)),
                ('weight', models.CharField(max_length=3)),
                ('position', models.CharField(max_length=15)),
                ('previous_teams', models.TextField(max_length=255)),
                ('college', models.CharField(max_length=50)),
                ('draft', models.CharField(max_length=50)),
                ('jersey', models.CharField(max_length=3)),
                ('playfrom', models.CharField(max_length=4)),
                ('playto', models.CharField(max_length=7)),
                ('info', models.TextField(max_length=1000)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('player_comments', models.ManyToManyField(related_name='player_commented', to='gsw.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replied_comment', to='gsw.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='reply',
            name='replier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reply', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='reply',
            name='reply_likes',
            field=models.ManyToManyField(related_name='liked_reply', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='player',
            name='player_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_created', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='player',
            name='player_replies',
            field=models.ManyToManyField(related_name='player_replied', to='gsw.Reply'),
        ),
        migrations.AddField(
            model_name='other',
            name='other_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_created', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='other',
            name='other_replies',
            field=models.ManyToManyField(related_name='other_replied', to='gsw.Reply'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_likes',
            field=models.ManyToManyField(related_name='liked_comment', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='coach',
            name='coach_comments',
            field=models.ManyToManyField(related_name='coach_commented', to='gsw.Comment'),
        ),
        migrations.AddField(
            model_name='coach',
            name='coach_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coach_created', to='gsw.User'),
        ),
        migrations.AddField(
            model_name='coach',
            name='coach_replies',
            field=models.ManyToManyField(related_name='coach_replied', to='gsw.Reply'),
        ),
        migrations.AddField(
            model_name='activity',
            name='act',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active', to='gsw.User'),
        ),
    ]
