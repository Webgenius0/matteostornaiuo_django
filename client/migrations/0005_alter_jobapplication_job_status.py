# Generated by Django 5.1.4 on 2025-02-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_jobtemplate_options_jobtemplate_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='job_status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('upcomming', 'UPCOMMING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED'), ('expired', 'EXPIRED')], default='PENDING', max_length=10),
        ),
    ]
