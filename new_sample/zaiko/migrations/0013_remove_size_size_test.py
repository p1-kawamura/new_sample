# Generated by Django 4.1.3 on 2023-04-19 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0012_size_size_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='size',
            name='size_test',
        ),
    ]
