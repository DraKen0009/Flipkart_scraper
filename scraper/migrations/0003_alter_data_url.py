# Generated by Django 4.2.4 on 2023-08-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('scraper', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]
