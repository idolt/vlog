# Generated by Django 3.0.8 on 2020-10-11 23:41

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlogsite', '0006_geton'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geton',
            name='time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='vlogtext',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
