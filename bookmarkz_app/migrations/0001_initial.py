# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-07 09:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to=settings.AUTH_USER_MODEL)),
                ('to_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SharedBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('votes', models.IntegerField(default=1)),
                ('bookmark', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bookmarkz_app.Bookmark')),
                ('users_voted', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('bookmarks', models.ManyToManyField(to='bookmarkz_app.Bookmark')),
            ],
        ),
        migrations.AddField(
            model_name='bookmark',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmarkz_app.Link'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('to_friend', 'from_friend')]),
        ),
    ]
