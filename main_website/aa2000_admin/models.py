from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
import os, random, string
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

# from .forms import BrandDetailForm


now = timezone.now()
# Create your models here.


def get_random_string(length=10):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(chars) for _ in range(length))


def admin_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = get_random_string()
    _now = datetime.now()
    
    return 'admins/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))

def brand_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = get_random_string()
    _now = datetime.now()
    
    return 'brands/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))

def product_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = get_random_string()
    _now = datetime.now()
    
    # Get model name and create a more user-friendly subfolder name
    model_name = instance.__class__.__name__.lower()
    subfolder_map = {
        'productphoto': 'photos',        # Main product photos
        'productdescription': 'descriptions',  # Description-related images
        'keyfeature': 'features'         # Key feature images
    }
    
    subfolder = subfolder_map.get(model_name, 'misc')
    
    # Get product ID - all models have a product relation
    if hasattr(instance, 'product'):
        product_id = instance.product.id
        product_slug = instance.product.product_slug
    else:
        product_id = 'new'
        product_slug = 'new'

    return 'products/{product_slug}/{subfolder}/{year}{month}-{productid}-{basename}-{randomstring}{ext}'.format(
        product_slug=product_slug,
        subfolder=subfolder,
        productid=product_id,
        basename=basefilename,
        randomstring=randomstr,
        ext=file_extension,
        year=_now.strftime('%Y'),
        month=_now.strftime('%m')
    )
    

def job_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = get_random_string()
    _now = datetime.now()
    
    return 'jobs/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))


def article_image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    randomstr = get_random_string()
    _now = datetime.now()
    
    return 'articles/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))


def inquiry_reply_attachment_uplaod(instance, filename):
    # basefilename, file_extension = os.path.splitext(filename)
    # randomstr = get_random_string()
    # _now = datetime.now()
    
    # return 'inquiry/{year}-{month}-{instance_id}-{basename}-{randomstring}{ext}'.format(instance_id = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))
    ticket_number = instance.inquiry_reply.inquiry.ticket
    return f'inquiry/{ticket_number}/{filename}'

def generate_ticket():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    while True:
        ticket = ''.join(random.choices(characters, k=12))  # Generate a 12-character string
        if not Inquiry.objects.filter(ticket=ticket).exists():
            return ticket









# models
class User(models.Model):
    username = models.CharField(max_length=255, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False,)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now = True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
    
class Role(models.Model):
    role_name = models.CharField(max_length=255, unique=True)
    role_description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.role_name
    

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user_role_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"
    
    
class AdminLevel(models.Model):
    admin_level_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.admin_level_name
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_code = models.CharField(max_length=6, unique=False)
    level = models.ForeignKey(AdminLevel, on_delete=models.DO_NOTHING)
    admin_fname = models.CharField(max_length=255, blank=False)
    admin_lname = models.CharField(max_length=255, blank=False)
    admin_email = models.EmailField(max_length=255, unique=True)
    admin_photo = models.ImageField(upload_to=admin_image_path, default='admins/aa2000_icon.png')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def image_tag(self):
        return mark_safe('<img src-"aa2000_admin/media/%a />'%self.admin_photo)
    
    def __str__(self):
        return self.admin_email
    
class System(models.Model):
    system_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.system_name
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True)
    brand_slug = models.SlugField(unique=True, max_length=200)
    system = models.ForeignKey(System, on_delete=models.DO_NOTHING)
    brand_logo = models.ImageField(upload_to=brand_image_path, default='brands/aa2000_icon.png')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def image_tag(self):
        return mark_safe('<img src-"aa2000_admin/media/%a />'%self.brand_logo)
    
    def __str__(self):
        return self.brand_slug
    
class BrandDetail(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name="brand_details")
    brand_description_1 = models.TextField(blank=True)
    brand_description_2 = models.TextField(blank=True)
    brand_image_1 = models.ImageField(upload_to=brand_image_path, blank=True)
    brand_image_2 = models.ImageField(upload_to=brand_image_path, blank=True)
    other_details = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
class ProductCategory(models.Model):
    system = models.ForeignKey(System, on_delete=models.DO_NOTHING, related_name="productCategory_system")
    category_name = models.TextField(blank=False)
    
    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=255 , blank=False)
    product_slug = models.SlugField(unique=True, max_length=200, blank=False)
    system = models.ForeignKey(System, on_delete=models.DO_NOTHING, related_name="product_system")
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, related_name="product_category", null=True)    
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, related_name="product_brand", null=True)
    short_description = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_slug
    
    
class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_photos")
    product_image = models.ImageField(upload_to=product_image_path, default='products/aa2000_icon.png')
    
class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_descriptions")
    product_description = models.TextField(blank=False)
    product_image = models.ImageField(upload_to=product_image_path, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_description
    
class KeyFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="key_features")
    key_feature = models.TextField(blank=False)
    key_feature_image = models.ImageField(upload_to=product_image_path, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key_feature
    
class TechSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_techSpec")
    tech_spec = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.tech_spec
    
class TechSpecDetails(models.Model):
    tech_spec = models.ForeignKey(TechSpec, on_delete=models.CASCADE, related_name="tech_spec_details")
    tech_spec_name = models.CharField(max_length=200, blank=False)
    tech_spec_value = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.tech_spec_name
    
    
class Job(models.Model):
    job_title = models.CharField(max_length=200, blank=False)
    job_slug = models.SlugField(unique=True, blank=False, max_length=200)
    job_image = models.ImageField(upload_to=job_image_path, default='jobs/aa2000_icon.png')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.job_title
    

class JobDescriptions(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="job_description")
    short_description = models.TextField(blank=False)
    long_description = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class JobResponsibilities(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_responsibilities")
    job_responsibility = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class JobQualifications(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_qualifications")
    job_qualification = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class JobPreferredSkills(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_preferred_skills")
    job_preferred_skill = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class JobCompensationBenefits(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="job_compensation_benefits")
    compensation = models.TextField(blank=False)
    benefits = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    


class Article(models.Model):
    article_title = models.CharField(max_length=200, blank=False)
    article_slug = models.SlugField(unique=True, blank=False, max_length=200)
    article_cover = models.ImageField(upload_to=article_image_path, default='articles/aa2000_icon.png') 
    keywords = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
class Author(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="article_author")
    author_name = models.CharField(max_length=200, blank=False)
    author_image = models.ImageField(upload_to=article_image_path, blank=True, default='articles/aa2000_icon.png')
    author_description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class ArticleContent(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="article_content")
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
class Action(models.Model):
    action_name = models.CharField(max_length=200, blank=False)
    action_description = models.TextField(blank=False)

    
class Entity(models.Model):
    entity_name = models.CharField(max_length=200, blank=False)
    entity_description = models.TextField(blank=False)

    
class AdminActivityLogs(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name="admin_on_activity")
    action = models.ForeignKey(Action, on_delete=models.DO_NOTHING, related_name="activity_action")
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, related_name="activity_entity")
    entity_item = models.IntegerField(blank=False, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    
class InquiryConcernCategory(models.Model):
    concern_category_name = models.TextField(blank=False)
    
    def __str__(self):
        return self.concern_category_name
    
class Inquiry(models.Model):
    ticket = models.CharField(max_length=12, unique=True, default=generate_ticket)
    status = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ticket
    
class InquiryDetails(models.Model):
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE, related_name="inquiry_details")
    fname = models.CharField(max_length=255, blank=False)
    lname = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    contact_num = models.CharField(max_length=11)
    concern_category = models.ForeignKey(InquiryConcernCategory, on_delete=models.DO_NOTHING, related_name="inquiry_concern_category")
    details = models.TextField(blank=True)
    preferred_contact_method = models.CharField(max_length=255)
    preferred_contact_time = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class Rfq(models.Model):
    inquiry_details = models.OneToOneField(InquiryDetails, on_delete=models.CASCADE, related_name='inquiry_rfq')
    project_name = models.CharField(max_length=255,blank=True)
    project_location = models.CharField(max_length=255,blank=True)
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    timeline = models.IntegerField(blank=True)
    additional_details = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    

class InquiryReply(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name="inquiry_reply")
    reply = models.TextField(blank=False)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, related_name='reply_admin_id')
    hasFile = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
class InquiryReplyAttachments(models.Model):
    inquiry_reply = models.ForeignKey(InquiryReply, on_delete=models.CASCADE, related_name='inquiry_reply_attachment')
    inquiry_attachment = models.FileField(upload_to=inquiry_reply_attachment_uplaod)
    
class GeneralVisit(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    visitor_id = models.CharField(max_length=255, default="visitor_00000")
    
    def __str__(self):
        return f"Visit by {self.visitor_id} at {self.timestamp}"
    
    
class EntityVisit(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, related_name="entity_visit")
    entity_item = models.IntegerField(blank=False, default=0)
    visitor_id = models.CharField(max_length=255, default="visitor_00000")