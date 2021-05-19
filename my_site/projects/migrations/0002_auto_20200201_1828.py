# Generated by Django 2.2.1 on 2020-02-02 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_abstract',
            field=models.TextField(max_length=1000),
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_text', models.CharField(max_length=50)),
                ('entry_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Entry')),
            ],
        ),
    ]
