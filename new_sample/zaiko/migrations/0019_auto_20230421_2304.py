# Generated by Django 3.1.7 on 2023-04-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0018_auto_20230421_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='busho',
            field=models.CharField(blank=True, max_length=30, verbose_name='所属'),
        ),
    ]
