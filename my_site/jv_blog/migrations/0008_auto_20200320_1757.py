# Generated by Django 2.1.15 on 2020-03-20 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jv_blog', '0007_auto_20200319_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='engry_show',
            new_name='entry_show',
        ),
    ]
