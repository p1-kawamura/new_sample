# Generated by Django 4.2.1 on 2023-05-16 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0033_category_alter_shouhin_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='shouhin',
            name='status',
            field=models.IntegerField(default=0, verbose_name='有効'),
        ),
    ]
