# Generated by Django 5.1.4 on 2025-02-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_staffreview_rating_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
