# Generated by Django 4.2.1 on 2023-05-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0035_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_banchi_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='番地_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_build_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='建物名_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_city_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='市区町村_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_com_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='会社名_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_cus_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='名前_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_deliday',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='配送指定日'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_pref_m',
            field=models.CharField(blank=True, max_length=10, verbose_name='都道府県_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_tel_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='電話番号_元'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='haisou_yubin_m',
            field=models.CharField(blank=True, max_length=30, verbose_name='郵便番号_元'),
        ),
    ]
