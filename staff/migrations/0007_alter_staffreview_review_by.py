# Generated by Django 5.1.4 on 2025-02-24 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_companyreview_options_and_more'),
        ('staff', '0006_alter_staffreview_review_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffreview',
            name='review_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.companyprofile'),
        ),
    ]
