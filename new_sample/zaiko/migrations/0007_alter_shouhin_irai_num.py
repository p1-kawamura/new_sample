# Generated by Django 4.1.3 on 2023-04-06 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0006_alter_shouhin_irai_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shouhin',
            name='irai_num',
            field=models.CharField(blank=True, default=0, max_length=10, verbose_name='依頼No'),
        ),
    ]
