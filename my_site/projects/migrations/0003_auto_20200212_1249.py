# Generated by Django 2.2.1 on 2020-02-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200201_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_thumbnail',
            field=models.ImageField(blank=True, default='projects/images/ivana-cajina-unsplash.jpg', upload_to='projects/images'),
        ),
    ]
