# Generated by Django 3.1.4 on 2021-01-15 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0003_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='link',
            field=models.TextField(blank=True),
        ),
    ]