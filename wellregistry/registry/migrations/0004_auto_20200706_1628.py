# Generated by Django 3.0.7 on 2020-07-06 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_country_lookups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='agency_med',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='registry',
            name='agency_nm',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='registry',
            name='alt_acy',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='registry',
            name='alt_datum_cd',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='registry',
            name='alt_method',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='registry',
            name='aqfr_char',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='registry',
            name='const_data_provider',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registry',
            name='country_cd',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='registry.CountryLookup'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='county_cd',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='registry',
            name='data_provider',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='registry',
            name='horz_acy',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='registry',
            name='horz_datum',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='registry',
            name='horz_method',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='registry',
            name='insert_user_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='registry',
            name='link',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='registry',
            name='lith_data_provider',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registry',
            name='local_aquifer_cd',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registry',
            name='local_aquifer_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='registry',
            name='nat_aqfr_desc',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='registry',
            name='nat_aquifer_cd',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='registry',
            name='pk_siteid',
            field=models.CharField(blank=True, max_length=37),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_data_provider',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_sys_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_chars',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_purpose',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_purpose_notes',
            field=models.CharField(blank=True, max_length=4000),
        ),
        migrations.AlterField(
            model_name='registry',
            name='qw_well_type',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='registry',
            name='review_flag',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='registry',
            name='site_name',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='registry',
            name='site_type',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='registry',
            name='state_cd',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='registry',
            name='update_user_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_data_provider',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_sys_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_chars',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_purpose',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_purpose_notes',
            field=models.CharField(blank=True, max_length=4000),
        ),
        migrations.AlterField(
            model_name='registry',
            name='wl_well_type',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
