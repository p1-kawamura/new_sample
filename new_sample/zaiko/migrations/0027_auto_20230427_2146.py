# Generated by Django 3.1.7 on 2023-04-27 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0026_alter_rireki_rental_unsou_com_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rireki_rental',
            name='password',
        ),
        migrations.AlterField(
            model_name='rental',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rireki_rental',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rireki_shouhin',
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
