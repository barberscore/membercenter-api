# Generated by Django 2.2.4 on 2019-08-19 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bhs', '0007_auto_20190819_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='representing',
            new_name='district',
        ),
    ]