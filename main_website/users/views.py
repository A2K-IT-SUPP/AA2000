from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from datetime import timedelta
import uuid

from aa2000_admin.models import System
from aa2000_admin.models import Brand
from aa2000_admin.models import BrandDetail

from aa2000_admin.models import ProductCategory
from aa2000_admin.models import Product
from aa2000_admin.models import ProductPhoto
from aa2000_admin.models import ProductDescription
from aa2000_admin.models import KeyFeature
from aa2000_admin.models import TechSpec
from aa2000_admin.models import TechSpecDetails

from aa2000_admin.models import Article
from aa2000_admin.models import ArticleContent
from aa2000_admin.models import Author

from aa2000_admin.models import Job
from aa2000_admin.models import JobDescriptions
from aa2000_admin.models import JobResponsibilities
from aa2000_admin.models import JobPreferredSkills
from aa2000_admin.models import JobQualifications
from aa2000_admin.models import JobCompensationBenefits

from aa2000_admin.models import InquiryConcernCategory
from aa2000_admin.models import Inquiry
from aa2000_admin.models import InquiryDetails
from aa2000_admin.models import Rfq
from aa2000_admin.models import InquiryReply
from aa2000_admin.models import InquiryReplyAttachments

from aa2000_admin.models import GeneralVisit
from aa2000_admin.models import EntityVisit


from aa2000_admin.email_utils import send_custom_email

# Create your views here.


def track_visit(request):
    visitor_id = request.COOKIES.get('visitor_id')

    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    today = timezone.now()
    one_hour_ago = today - timedelta(hours=1)
    # print(today)

    visit = GeneralVisit.objects.filter(visitor_id=visitor_id, timestamp__gte=one_hour_ago).first()
    
    if not visit:   
        GeneralVisit.objects.create(visitor_id=visitor_id)
        print("New visit added for visitor:", visitor_id)
    else:
        print("Visitor already visited within the last hour:", visitor_id)


    return visitor_id  



def entity_track_visit(request, entity, entity_item):
    visitor_id = request.COOKIES.get('visitor_id')
    
    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    today = timezone.now()
    one_hour_ago = today - timedelta(hours=1)
    
    entity_visit = EntityVisit.objects.filter(visitor_id=visitor_id, entity_id=entity, entity_item=entity_item, timestamp__gte=one_hour_ago).first()

    if not entity_visit:
        EntityVisit.objects.create(
            visitor_id=visitor_id,
            entity_id=entity,
            entity_item=entity_item
        )
        print("New visit added for visitor:", visitor_id)
    else:
        print("Visitor already visited within the last hour:", visitor_id)
        


def index(request):
    
    visitor_id = track_visit(request)  

    brands = Brand.objects.all().order_by('id')
    articles = Article.objects.select_related('article_author', 'article_content').order_by('-modified_at')[:5]

    page_obj = {
        'brands': brands,
        'articles': articles
    }

    response = render(request, 'users/index.html', page_obj)

    if visitor_id:
            response.set_cookie(
                'visitor_id', 
                visitor_id, 
                max_age=365*24*60*60,  
                httponly=True,  
                samesite='Lax'
            )

    return response



def about(request):
    return render(request, 'users/about.html')


# systems pages
def systems(request):
    return render(request, 'users/systems.html')

def systems_fdas(request):
    brands = Brand.objects.filter(system_id=1)
    
    page_obj = {
        'brands': brands
    }
    
    return render(request, 'users/systems/systems-fdas.html', page_obj)

def systems_afss(request):
    
    brands = Brand.objects.filter(system_id=2)
    
    page_obj = {
        'brands': brands
    }
    
    return render(request, 'users/systems/systems-afss.html', page_obj)

def systems_cctv(request):
        
    brands = Brand.objects.filter(system_id=3)
    
    page_obj = {
        'brands': brands
    }
    
    return render(request, 'users/systems/systems-cctv.html', page_obj)

def systems_access_control(request):
    
    brands = Brand.objects.filter(system_id=4)
    
    page_obj = {
        'brands': brands
    }
    
    return render(request, 'users/systems/systems-access-control.html', page_obj)

def systems_burglar_alarm(request):
    brands = Brand.objects.filter(system_id=5)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-burglar-alarm.html', page_obj)

def systems_paging(request):
    brands = Brand.objects.filter(system_id=6)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-paging.html', page_obj)

def systems_walkthrough_metal_detectors(request):
    brands = Brand.objects.filter(system_id=7)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-walkthrough-metal-detectors.html', page_obj)

def systems_gate_barriers(request):
    brands = Brand.objects.filter(system_id=8)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-gate-barriers.html', page_obj)

def systems_room_alert(request):
    brands = Brand.objects.filter(system_id=12)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-room-alert.html', page_obj)

def systems_xray_scanners(request):
    brands = Brand.objects.filter(system_id=10)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-xray-scanners.html', page_obj)

def systems_eas(request):
    brands = Brand.objects.filter(system_id=9)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-eas.html', page_obj)

def systems_led(request):
    brands = Brand.objects.filter(system_id=11)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-led.html', page_obj)

def systems_robots(request):
    brands = Brand.objects.filter(system_id=13)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-robots.html', page_obj)

def systems_erp(request):
    brands = Brand.objects.filter(system_id=14)
    
    page_obj = {
        'brands': brands
    }
    return render(request, 'users/systems/systems-erp.html', page_obj)


# products pages
def products(request):
    
    system = request.GET.get('system')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    
    products = Product.objects.select_related(
        'system', 'category', 'brand'
    ).prefetch_related(
        'product_photos',
    )
    
    system_filter = {
            'fdas': 1,
            'afss': 2,
            'cctv': 3,
            'access-control': 4,
            'burglar-alarm': 5,
            'intercom-paging': 6,
            'walkthrough-metal-detectors': 7,
            'gate-barriers': 8,
            'eas': 9,
            'xray-baggage-scanners': 10,
            'led': 11,
            'room-alert': 12,
            'robots': 13,
            'erp': 14,
        }
    
    categories = ProductCategory.objects.none()
    brands = Brand.objects.none()
    
    
    system_id = system_filter.get(system)
    if system_id:
        products = products.filter(system_id=system_id)
        categories = ProductCategory.objects.filter(system_id=system_id)
        brands = Brand.objects.filter(system_id=system_id)
    else:
        system = 'ALL AA2000'
    

    if category:
        products = products.filter(category_id=category)
    if brand:
        products = products.filter(brand_id=brand)
        
    formatted_system = system.replace("-", " ").upper()
    


    # if search is applied
    search_product = request.GET.get('search_product', '')
    sort_by = request.GET.get('sort_by', 'name-up')
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    
    if search_product:
        products = products.filter(Q(product_name__icontains=search_product) | Q(short_description__icontains=search_product))
    
    if sort_by == 'name-up':
        products = products.order_by('product_name')
    elif sort_by == 'name-down':
        products = products.order_by('-product_name')
        
    if selected_categories:
        products = products.filter(category_id__in=selected_categories)
        
    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)
    
    
    # paginator = Paginator(products, 12)
    # page_number = request.GET.get('page')
    # products = paginator.get_page(page_number)
    
    page_obj = {
        'products': products,
        'formatted_system': formatted_system,
        'categories': categories,
        'brands': brands,
    }
            
    return render(request, 'users/products.html', page_obj)

def product_overview(request, slug):
    
    productData = Product.objects.select_related(
        'brand',
        'system',
        'category'
    ). prefetch_related(
        'product_photos',
        'product_descriptions',
        'key_features',
        Prefetch(
            'product_techSpec',
            queryset=TechSpec.objects.prefetch_related('tech_spec_details')
        )
    ).get(product_slug=slug)
    
    productPhotos = productData.product_photos.all()
    productDescriptions = productData.product_descriptions.all()
    productKeyFeatures = productData.key_features.all()
    productTechSpecs = productData.product_techSpec.all()
    
    similarProducts = Product.objects.filter(system_id=productData.system_id, category_id=productData.category_id)[:15]
    similarBrand = Product.objects.filter(brand_id=productData.brand_id)[:15]
    
    page_obj = {
        'productData': productData,
        'productPhotos': productPhotos,
        'productDescriptions': productDescriptions,
        'productKeyFeatures': productKeyFeatures,
        'productTechSpecs': productTechSpecs,
        'similarProducts': similarProducts,
        'similarBrand': similarBrand
    }
    
    
    entity_track_visit(request, 4, productData.id)
    
    return render(request, 'users/product-overview.html', page_obj)



# services
def services(request):
    return render(request, 'users/services.html')

def services_supply(request):
    return render(request, 'users/services/services-supply.html')

def services_installation(request):
    return render(request, 'users/services/services-installation.html')

def services_maintenance(request):
    return render(request, 'users/services/services-maintenance.html')

def services_troubleshooting(request):
    return render(request, 'users/services/services-troubleshooting.html')

def services_design(request):
    return render(request, 'users/services/services-design.html')

def services_inspection(request):
    return render(request, 'users/services/services-inspection.html')

def services_consultation(request):
    return render(request, 'users/services/services-consultation.html')

def services_training(request):
    return render(request, 'users/services/services-training.html')


def services_electrical(request):
    return render(request, 'users/services/services-electrical.html')

def services_mechanical(request):
    return render(request, 'users/services/services-mechanical.html')

def services_plumbing(request):
    return render(request, 'users/services/services-plumbing.html')

def services_fitout(request):
    return render(request, 'users/services/services-fitout.html')

def services_aircon(request):
    return render(request, 'users/services/services-aircon.html')

def services_fire_safety(request):
    return render(request, 'users/services/services-fire-safety.html')

def services_bms(request):
    return render(request, 'users/services/services-bms.html')

def services_elevator(request):
    return render(request, 'users/services/services-elevator.html')

def services_energy(request):
    return render(request, 'users/services/services-energy.html')


def services_data_cabling(request):
    return render(request, 'users/services/services-data-cabling.html')



# brands
def brands(request):
    
    brands = Brand.objects.all()

    system = request.GET.get('system')    
        
    if system:
        system_filter = {
            'fdas': 1,
            'afss': 2,
            'cctv': 3,
            'access-control': 4,
            'burglar-alarm': 5,
            'intercom-paging': 6,
            'walkthrough-metal-detectors': 7,
            'gate-barriers': 8,
            'eas': 9,
            'xray-baggage-scanners': 10,
            'led': 11,
            'room-alert': 12,
            'robots': 13,
            'erp': 14,
        }
        system_id = system_filter.get(system)
        if system_id:
            brands = Brand.objects.filter(system_id=system_id)
    else:
        system = 'all trusted'
        
    formatted_system = system.replace("-", " ").title()
    page_obj = {
        'formatted_system': formatted_system,
        'brands': brands,
    }
    
    return render(request, 'users/brands.html', page_obj)

def brands_overview(request, slug):
    
    brand = Brand.objects.select_related('brand_details').get(brand_slug=slug)
    products = Product.objects.select_related('system', 'category', 'brand').prefetch_related('product_photos').filter(brand=brand)[:10]
    
    page_obj = {
        'brand': brand,
        'products': products,
    }
    entity_track_visit(request, 3, brand.id)
    return render(request, 'users/brands-overview.html' , page_obj)


# careers
def careers(request):
    
    jobs = Job.objects.prefetch_related('job_description').all().order_by('-modified_at')
    page_obj = {
        'jobs': jobs,
    }
    return render(request, 'users/careers.html', page_obj)

def careers_overview(request, slug):
    
    jobData = Job.objects.prefetch_related(
        'job_description',
        'job_responsibilities',
        'job_qualifications',
        'job_preferred_skills',
        'job_compensation_benefits'
    ).get(job_slug=slug)
    
    page_obj = {
        'jobData': jobData,
    }
    
    return render(request, 'users/careers-overview.html', page_obj)


# articles
def articles(request):
    
    articles = Article.objects.select_related('article_author', 'article_content').order_by('-modified_at')[:5]
    
    page_obj = {
        'articles': articles,
    }
    
    return render(request, 'users/articles.html', page_obj)

def blogs(request):
    
    articles = Article.objects.select_related('article_author', 'article_content').order_by('-modified_at')
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    page_obj = {
        'articles': articles,
    }
    
    return render(request, 'users/blogs.html', page_obj)

def policy(request):
    return render(request, 'users/policy.html')

def faqs(request):
    return render(request, 'users/faqs.html')

def articles_view(request, slug):
    articles = Article.objects.select_related(
        'article_author',
        'article_content'
        ).get(article_slug=slug)
    
    page_obj = {
        'articleData': articles,
    }
    entity_track_visit(request, 5, articles.id)
    return render(request, 'users/articles-view.html', page_obj)




#contact
def contact(request):
    return render(request, 'users/contact.html')


def submit_inquiry(request):
    try:
        
        inquiryData = request.POST
        concernType = inquiryData.get('typeOfConcern')
        
        inquiry = Inquiry.objects.create(
            status='NEW'
        )
        
        inquiry_details = InquiryDetails.objects.create(
            inquiry=inquiry,
            fname=inquiryData.get('firstName'),
            lname=inquiryData.get('lastName'),
            email=inquiryData.get('email'),
            contact_num=inquiryData.get('contactNumber'),
            concern_category_id=concernType,
            details=inquiryData.get('inquiry'),
            preferred_contact_method=inquiryData.get('preferredContactMethod'),
            preferred_contact_time=inquiryData.get('preferredContactTime')        
        )
        
        if concernType == '1':
            Rfq.objects.create(
                inquiry_details=inquiry_details,
                project_name=inquiryData.get('projectName'),
                project_location=inquiryData.get('projectLocation'),
                estimated_budget=inquiryData.get('estimatedBudget'),
                timeline=inquiryData.get('timeline'),
                additional_details=inquiryData.get('additionalDetails')
            )
            

        status_link = f"http://127.0.0.1:8000/inquiry/status?ticket={inquiry.ticket}"
        send_custom_email(
            user=inquiry_details,
            email_type='inquiry_confirmation',
            ticket_id=inquiry.ticket,
            status_link=status_link,
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Inquiry submitted successfully',
            'ticket': inquiry.ticket
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def ticket(request):
    ticket_id = request.GET.get('ticket')  # Get the ticket_id from URL query params
    context = {}

    if ticket_id:
        try:
            # Retrieve the Inquiry with its related InquiryDetails and Rfq
            inquiry = Inquiry.objects.select_related('inquiry_details__inquiry_rfq').get(ticket=ticket_id)

            # Access related details
            inquiry_details = inquiry.inquiry_details
            rfq = inquiry_details.inquiry_rfq if hasattr(inquiry_details, 'inquiry_rfq') else None

            # Prepare the context with the relevant information
            context = {
                'status': 'success',
                'ticket_id': ticket_id,
                'inquiry': inquiry,
                'inquiry_details': inquiry_details,
                'rfq': rfq,
            }
        except Inquiry.DoesNotExist:
            context = {
                'status': 'error',
                'message': 'Ticket not found'
            }
    
    return render(request, 'users/ticket.html', context)
