# Generated by Django 2.1.15 on 2020-03-30 00:17

from django.db import migrations, models
import jv_blog.models_helper


class Migration(migrations.Migration):

    dependencies = [
        ('jv_blog', '0008_auto_20200320_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='raw_entry',
            field=models.FileField(blank=True, upload_to=jv_blog.models_helper.raw_directory_path),
        ),
    ]
