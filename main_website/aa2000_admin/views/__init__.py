



#home views 
from .home_views import (
    home,
    dashboard_data
) 


# index views
from .index_views import(
    index,
    login,
    logout,
)


# admin views
from .admins_views import (
    admins,
    add_admin,
    processadd_admin,
    view_admin,
    edit_admin,
    edit_admin_credentials,
    edit_admin_access_code,
    delete_admin,
)


# articles views
from .articles_views import (
    articles,
    add_article,
    view_article,
    processadd_article,
    edit_article,
    delete_article,
)


# brands views
from .brands_views import (
    brands,
    add_brand,
    processadd_brand,
    view_brand,
    edit_brand,
    delete_brand,
)


# inquiries views  
from .inquiries_views import (
    inquiries,
    view_inquiry,
    reply_inquiry
)

# jobs views
from .jobs_views import (
    jobs,
    add_job,
    view_job,
    processadd_job,
    edit_job,
    delete_job
)

# logs views
from .logs_views import (
    logs,
)


# products views 
from .products_views import (
    get_categories,
    products,
    add_product,
    add_product_overview,
    add_product_photos,
    add_product_description,
    add_product_technical_specs,
    add_product_key_features,
    view_product,
    edit_product_overview,
    edit_product_photos,
    edit_product_description,
    edit_product_technical_specs,
    edit_product_key_features,
    delete_product,
)


# reports views
from .reports_views import (
    reports,
    reports_get_products_data,
    reports_get_brands_data,
    reports_get_articles_data,
    reports_get_inquiries_data,
)


# settings views
from .settings_views import (
    admin_settings,
    edit_admin_settings,
    edit_credentials_admin_settings,
    edit_access_code_admin_settings,
)



from .uploads_views import (
    upload_image,
)
