# Generated by Django 3.1.7 on 2023-04-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0017_shozoku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rireki_rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('irai_num', models.IntegerField(verbose_name='依頼No')),
                ('irai_type', models.IntegerField(verbose_name='内容')),
                ('rental_day', models.DateField(auto_now_add=True, verbose_name='貸出日')),
                ('shozoku', models.CharField(blank=True, max_length=30, verbose_name='所属')),
                ('tantou', models.CharField(blank=True, max_length=30, verbose_name='担当者')),
                ('haisou_tempo', models.CharField(blank=True, max_length=30, verbose_name='配送店舗')),
                ('haisou_com', models.CharField(blank=True, max_length=30, verbose_name='会社名')),
                ('haisou_cus', models.CharField(blank=True, max_length=30, verbose_name='名前')),
                ('haisou_yubin', models.CharField(blank=True, max_length=30, verbose_name='郵便番号')),
                ('haisou_adress', models.CharField(blank=True, max_length=100, verbose_name='住所')),
                ('haisou_tel', models.CharField(blank=True, max_length=30, verbose_name='電話番号')),
                ('haisou_mail', models.CharField(blank=True, max_length=100, verbose_name='メールアドレス')),
                ('nouhin_com', models.CharField(blank=True, max_length=30, verbose_name='納品書会社名')),
                ('nouhin_cus', models.CharField(blank=True, max_length=30, verbose_name='納品書名前')),
                ('nouhin_day', models.DateField(blank=True, default='', null=True, verbose_name='納品書日付')),
                ('bikou1', models.TextField(blank=True, verbose_name='備考1')),
                ('bikou2', models.TextField(blank=True, verbose_name='備考2')),
            ],
        ),
        migrations.RemoveField(
            model_name='rental',
            name='bikou1',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='bikou2',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='nouhin_day',
        ),
        migrations.AlterField(
            model_name='rental',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shozoku',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='size',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]