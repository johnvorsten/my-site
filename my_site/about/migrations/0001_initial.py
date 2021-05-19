# Generated by Django 2.1.15 on 2020-03-19 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('profile_picture', models.CharField(choices=[('/media/about\\images\\○ Headshot 2 v1.jpg', 'Headshot v1'), ('/media/about\\images\\○ Headshot 2 v1 zoom.jpg', 'Headshot v1 zoom'), ('/media/about\\images\\○ Headshot 2 unfilter.jpg', 'Headshot v1 unfiltered'), ('/media/about\\images\\○ Headshot 2 unfilter sq.jpg', 'Headshot unfiltered square')], default=('/media/', 'about', 'images', '○ Headshot 2 unfilter sq.jpg'), max_length=200)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('project_description', models.CharField(max_length=150)),
                ('project_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='about.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=50)),
                ('skill_description', models.CharField(max_length=150)),
                ('skill_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='about.Profile')),
            ],
        ),
    ]
