# Generated by Django 4.1.3 on 2023-04-06 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0002_alter_shouhin_irai_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shouhin',
            name='irai_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='依頼No'),
        ),
    ]
