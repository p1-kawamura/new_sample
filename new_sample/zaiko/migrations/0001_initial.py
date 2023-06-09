# Generated by Django 4.1.3 on 2023-04-05 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shouhin',
            fields=[
                ('hontai_num', models.AutoField(primary_key=True, serialize=False, verbose_name='本体No')),
                ('sample_num', models.CharField(blank=True, max_length=20, verbose_name='サンプルNo')),
                ('category', models.CharField(blank=True, max_length=10, verbose_name='カテゴリ')),
                ('shouhin_num', models.CharField(blank=True, max_length=20, verbose_name='商品番号')),
                ('brand', models.CharField(blank=True, max_length=20, verbose_name='ブランド')),
                ('shouhin_name', models.CharField(blank=True, max_length=255, verbose_name='商品名')),
                ('color', models.CharField(blank=True, max_length=255, verbose_name='カラー')),
                ('size', models.CharField(blank=True, max_length=20, verbose_name='サイズ')),
                ('size_num', models.IntegerField(null=True, verbose_name='サイズ値')),
                ('kakou', models.CharField(blank=True, max_length=50, verbose_name='加工')),
                ('bikou', models.CharField(blank=True, max_length=255, verbose_name='備考')),
                ('touroku_day', models.DateField(null=True, verbose_name='登録日')),
                ('koushin_day', models.DateField(auto_now=True, verbose_name='更新日')),
                ('joutai', models.CharField(blank=True, max_length=10, verbose_name='状態')),
                ('irai_num', models.IntegerField(verbose_name='依頼No')),
            ],
        ),
        migrations.CreateModel(
            name='rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_day', models.DateField(null=True, verbose_name='貸出日')),
                ('busho', models.CharField(blank=True, max_length=30, verbose_name='部署')),
                ('tantou', models.CharField(blank=True, max_length=30, verbose_name='担当者')),
                ('com_name', models.CharField(blank=True, max_length=30, verbose_name='会社名')),
                ('cus_name', models.CharField(blank=True, max_length=30, verbose_name='名前')),
                ('nouhin_day', models.DateField(null=True, verbose_name='納品書日付')),
                ('bikou1', models.TextField(blank=True, verbose_name='備考1')),
                ('bikou2', models.TextField(blank=True, verbose_name='備考2')),
                ('irai_num_rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaiko.shouhin', verbose_name='依頼No')),
            ],
        ),
    ]
