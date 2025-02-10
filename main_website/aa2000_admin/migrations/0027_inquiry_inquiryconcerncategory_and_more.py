# Generated by Django 5.1.2 on 2024-11-11 18:02

import aa2000_admin.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa2000_admin', '0026_branddetail_other_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(default=aa2000_admin.models.generate_ticket, max_length=12, unique=True)),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InquiryConcernCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concern_category_name', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='techspec',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_techSpec', to='aa2000_admin.product'),
        ),
        migrations.CreateModel(
            name='InquiryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('contact_num', models.CharField(max_length=11)),
                ('details', models.TextField(blank=True)),
                ('preferred_contact_method', models.CharField(max_length=255)),
                ('preferred_contact_time', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('concern_category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inquiry_concern_category', to='aa2000_admin.inquiryconcerncategory')),
                ('inquiry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_details', to='aa2000_admin.inquiry')),
            ],
        ),
        migrations.CreateModel(
            name='InquiryReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('hasFile', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply_admin_id', to='aa2000_admin.admin')),
                ('inquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_reply', to='aa2000_admin.inquiry')),
            ],
        ),
        migrations.CreateModel(
            name='InquiryReplyAttachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquiry_attachment', models.FileField(upload_to=aa2000_admin.models.inquiry_reply_attachment_uplaod)),
                ('inquiry_reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_reply_attachment', to='aa2000_admin.inquiryreply')),
            ],
        ),
        migrations.CreateModel(
            name='Rfq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=255)),
                ('project_location', models.CharField(blank=True, max_length=255)),
                ('estimated_budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('timeline', models.IntegerField(blank=True)),
                ('additional_details', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('inquiry_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_rfq', to='aa2000_admin.inquirydetails')),
            ],
        ),
    ]
