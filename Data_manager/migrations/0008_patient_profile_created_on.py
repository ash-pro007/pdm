# Generated by Django 5.0.6 on 2024-10-22 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data_manager', '0007_alter_patient_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='profile_created_on',
            field=models.DateField(default='2024-01-01'),
            preserve_default=False,
        ),
    ]