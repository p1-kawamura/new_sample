# Generated by Django 4.2.1 on 2023-06-20 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0040_rireki_shouhin_henkyaku_rireki_shouhin_henkyaku_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='rental_day',
            field=models.DateField(default='', verbose_name='貸出日'),
        ),
    ]
