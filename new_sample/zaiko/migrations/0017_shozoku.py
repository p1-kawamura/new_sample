# Generated by Django 4.1.3 on 2023-04-21 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiko', '0016_delete_shozoku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shozoku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shozoku', models.CharField(max_length=30, verbose_name='所属')),
            ],
        ),
    ]
