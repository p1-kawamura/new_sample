# Generated by Django 3.1.7 on 2023-04-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0020_auto_20230421_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rireki_rental',
            name='bikou1',
            field=models.TextField(blank=True, verbose_name='備考（納品）'),
        ),
        migrations.AlterField(
            model_name='rireki_rental',
            name='bikou2',
            field=models.TextField(blank=True, verbose_name='備考（依頼）'),
        ),
    ]
