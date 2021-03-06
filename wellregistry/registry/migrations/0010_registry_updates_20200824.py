# The below suppresses pylint message: Module name "*" doesn't conform to snake_case naming style
# pylint: disable-msg=C0103
# Enable check for the rest of the file
# pylint: enable-msg=C0103
"""
# Changes to the Registry model
"""
# Generated by Django 3.1 on 2020-08-24 19:19

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Defines the migrations for updating the Registry model.
    """
    dependencies = [
        ('registry', '0009_registry_updates_20200819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='qw_well_chars',
            field=models.CharField(blank=True, choices=[('Background', 'Background'), ('Suspected/Anticipated Changes', 'Suspected/Anticipated Changes'), ('Known Changes', 'Known Changes')], max_length=32, verbose_name='QW well characteristics'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_purpose',
            field=models.CharField(blank=True, choices=[('Dedicated Monitoring/Observation', 'Dedicated Monitoring/Observation'), ('Other', 'Other')], max_length=32, verbose_name='QW well purpose'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_type',
            field=models.CharField(blank=True, choices=[('Surveillance', 'Surveillance'), ('Trend', 'Trend'), ('Special', 'Special')], max_length=32, verbose_name='QW well type'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_chars',
            field=models.CharField(blank=True, choices=[('Background', 'Background'), ('Suspected/Anticipated Changes', 'Suspected/Anticipated Changes'), ('Known Changes', 'Known Changes')], max_length=32, verbose_name='WL well characteristics'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_purpose',
            field=models.CharField(blank=True, choices=[('Dedicated Monitoring/Observation', 'Dedicated Monitoring/Observation'), ('Other', 'Other')], max_length=32, verbose_name='WL well purpose'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_type',
            field=models.CharField(blank=True, choices=[('Surveillance', 'Surveillance'), ('Trend', 'Trend'), ('Special', 'Special')], max_length=32, verbose_name='WL well type'),
        ),
    ]
