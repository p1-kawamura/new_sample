# Generated by Django 4.1.3 on 2023-04-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0024_alter_rental_rental_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='rireki_rental',
            name='unsou_com',
            field=models.CharField(default='', max_length=20, verbose_name='運送会社'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='unsou_num',
            field=models.CharField(default='', max_length=20, verbose_name='問い合わせ番号'),
        ),
    ]
