# Generated by Django 2.0.5 on 2018-05-29 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='pu_date',
            new_name='pub_date',
        ),
    ]
