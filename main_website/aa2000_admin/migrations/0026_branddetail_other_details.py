# Generated by Django 5.1.2 on 2024-11-09 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa2000_admin', '0025_article_article_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='branddetail',
            name='other_details',
            field=models.TextField(blank=True),
        ),
    ]
