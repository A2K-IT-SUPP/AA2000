from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name = 'aa2000_admin'

urlpatterns = [
    path('', index, name='index'),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    
    path('home', home, name="home"),
    path('home/get/data/dashboard', dashboard_data, name="dashboard_data"),
    
    path('inquiries', inquiries, name="inquiries"),
    path('inquiries/<slug:slug>/view', view_inquiry, name="view_inquiry"),
    path('inquiries/<slug:slug>/reply', reply_inquiry, name="reply_inquiry"),
    
    path('brands', brands, name="brands"),    
    path('brands/add', add_brand, name="add_brand"),
    path('brands/processadd', processadd_brand, name="processadd_brand"),
    path('brands/<slug:slug>/view', view_brand, name="view_brand"),
    path('brands/<slug:slug>/edit', edit_brand, name="edit_brand"),
    path('brands/<slug:slug>/delete', delete_brand, name="delete_brand"),
    
    
    # get the systems data
    # path('systems', get_systems, name="get_systems"),
    path('systems/category', get_categories, name="get_categories"),

    
    path('products', products, name="products"),
    path('products/add', add_product, name="add_product"),
    path('products/add/product_overview', add_product_overview, name='add_product_overview'),
    path('products/add/product_photos', add_product_photos, name="add_product_photos"),
    path('products/add/product_description', add_product_description, name="add_product_description"),
    path('products/add/product_key_features', add_product_key_features, name="add_product_key_features"),
    path('products/add/product_technical_specs', add_product_technical_specs, name="add_product_technical_specs"),
    path('products/<slug:slug>/view', view_product, name="view_product"),
    path('products/edit/<slug:slug>/product_overview', edit_product_overview, name='edit_product_overview'),
    path('products/edit/<slug:slug>/product_photos', edit_product_photos, name="edit_product_photos"),
    path('products/edit/<slug:slug>/product_description', edit_product_description, name="edit_product_description"),
    path('products/edit/<slug:slug>/product_key_features', edit_product_key_features, name="edit_product_key_features"),
    path('products/edit/<slug:slug>/product_technical_specs', edit_product_technical_specs, name="edit_product_technical_specs"),
    path('products/delete/<slug:slug>', delete_product, name="delete_product"),

    path('jobs', jobs, name="jobs"),
    path('jobs/add', add_job, name="add_job"),
    path('jobs/processadd', processadd_job, name="processadd_job"),
    path('jobs/<slug:slug>/view', view_job, name="view_job"),
    path('jobs/<slug:slug>/edit', edit_job, name="edit_job"),
    path('jobs/delete/<slug:slug>', delete_job, name="delete_job"),

    path('articles', articles, name="articles"),
    path('articles/add', add_article, name="add_article"),
    path('articles/processadd', processadd_article, name="processadd_article"),
    path('articles/<slug:slug>/view', view_article, name="view_article"),
    path('articles/<slug:slug>/edit', edit_article, name="edit_article"),
    path('articles/<slug:slug>/delete', delete_article, name="delete_article"),
    
    path('admins', admins, name="admins"),
    # path('search', search, name="search"),
    path('admins/add', add_admin, name="add_admin"),
    path('admins/processadd', processadd_admin, name="processadd_admin"),
    path('admins/<int:admin_id>/view', view_admin, name="view_admin"),
    path('admins/<int:admin_id>/edit', edit_admin, name="edit_admin"),
    path('admins/<int:admin_id>/edit/credentials', edit_admin_credentials, name="edit_admin_credentials"),
    path('admins/<int:admin_id>/edit/access_code', edit_admin_access_code, name="edit_admin_access_code"),
    path('admins/<int:admin_id>/delete', delete_admin, name="delete_admin"),
    
    path('reports', reports, name="reports"),
    path('reports/get/data/products', reports_get_products_data, name="reports_get_products_data"),
    path('reports/get/data/brands', reports_get_brands_data, name="reports_get_brands_data"),
    path('reports/get/data/articles', reports_get_articles_data, name="reports_get_articles_data"),
    path('reports/get/data/inquiries', reports_get_inquiries_data, name="reports_get_inquiries_data"),
    
    
    
    
    path('logs', logs, name="logs"),
    
    path('settings', admin_settings, name="admin_settings"),
    path('settings/edit', edit_admin_settings, name="edit_admin_settings"),
    path('settings/edit/credentials', edit_credentials_admin_settings, name="edit_credentials_admin_settings"),
    path('settings/edit/access_code', edit_access_code_admin_settings, name="edit_access_code_admin_settings"),
    
    path('upload', upload_image, name='upload_image'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

