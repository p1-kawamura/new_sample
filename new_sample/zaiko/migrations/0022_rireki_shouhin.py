# Generated by Django 3.1.7 on 2023-04-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0021_auto_20230421_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rireki_shouhin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('irai_num', models.IntegerField(verbose_name='依頼No')),
                ('irai_hontai_num', models.IntegerField(verbose_name='本体No')),
            ],
        ),
    ]
