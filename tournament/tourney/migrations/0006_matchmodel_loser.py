# Generated by Django 3.0.5 on 2020-04-17 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0005_auto_20200413_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchmodel',
            name='loser',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]