# Generated by Django 3.1.3 on 2020-12-04 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PickAppDemo', '0003_auto_20201203_1305'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='Orders',
        ),
    ]
