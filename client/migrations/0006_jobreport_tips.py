# Generated by Django 5.1.4 on 2025-02-24 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_companyreview_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobreport',
            name='tips',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
