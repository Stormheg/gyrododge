# Generated by Django 3.1.1 on 2020-09-10 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='name',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
    ]
