# Generated by Django 4.1.3 on 2023-04-06 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0004_alter_shouhin_irai_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shouhin',
            name='irai_num',
            field=models.IntegerField(default=0, verbose_name='依頼No'),
        ),
    ]
