# Generated by Django 5.1.2 on 2024-11-03 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa2000_admin', '0016_alter_job_job_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcompensationbenefits',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_compensation_benefits', to='aa2000_admin.job'),
        ),
        migrations.AlterField(
            model_name='jobdescriptions',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_description', to='aa2000_admin.job'),
        ),
    ]
