# Generated by Django 5.1.2 on 2024-11-01 04:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa2000_admin', '0013_alter_admin_created_at_alter_brand_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdescription',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_descriptions', to='aa2000_admin.product'),
        ),
    ]
