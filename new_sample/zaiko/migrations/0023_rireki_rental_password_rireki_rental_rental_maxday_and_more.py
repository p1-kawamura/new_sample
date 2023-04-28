# Generated by Django 4.1.3 on 2023-04-24 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0022_rireki_shouhin'),
    ]

    operations = [
        migrations.AddField(
            model_name='rireki_rental',
            name='password',
            field=models.CharField(default='', max_length=20, verbose_name='パスワード'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='rental_maxday',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='貸出期限'),
        ),
        migrations.AddField(
            model_name='rireki_rental',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状態'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rireki_rental',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rireki_rental',
            name='nouhin_day',
            field=models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='納品書日付'),
        ),
        migrations.AlterField(
            model_name='rireki_shouhin',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shozoku',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='size',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]