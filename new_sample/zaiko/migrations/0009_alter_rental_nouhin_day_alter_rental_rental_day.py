# Generated by Django 4.1.3 on 2023-04-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0008_alter_rental_irai_num_rental_alter_rental_nouhin_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='nouhin_day',
            field=models.DateField(blank=True, default='', null=True, verbose_name='納品書日付'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='rental_day',
            field=models.DateField(blank=True, default='', null=True, verbose_name='貸出日'),
        ),
    ]
