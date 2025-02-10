from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, OuterRef, Subquery, F, DateField
from django.db.models.functions import TruncDate, Extract, Cast
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from ..models import User
from ..models import Role
from ..models import UserRole
from ..models import AdminLevel
from ..models import Admin

from ..models import System
from ..models import Brand
from ..models import BrandDetail
from ..models import ProductCategory
from ..models import Product
from ..models import ProductPhoto
from ..models import ProductDescription
from ..models import KeyFeature
from ..models import TechSpec
from ..models import TechSpecDetails

from ..models import Article
from ..models import ArticleContent
from ..models import Author

from ..models import InquiryConcernCategory
from ..models import Inquiry
from ..models import InquiryDetails
from ..models import Rfq
from ..models import InquiryReply
from ..models import InquiryReplyAttachments

from ..models import Job
from ..models import JobDescriptions
from ..models import JobResponsibilities
from ..models import JobPreferredSkills
from ..models import JobQualifications
from ..models import JobCompensationBenefits

from ..models import GeneralVisit
from ..models import EntityVisit

from .logs_views import record_log, get_recent_activities


def home(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user) 
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Dashboard',
                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            return render(request, 'aa2000_admin/home.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')

    # return render(request, 'aa2000_admin/home.html', page_details)


def dashboard_data(request):
    try:
        current_datetime = timezone.now()
        seven_days_before_datetime = current_datetime - timedelta(days=7)
                
        total_products_count = Product.objects.all().count()
        count_change_product = Product.objects.filter(created_at__range=[seven_days_before_datetime, current_datetime]).count()
        count_change_product_percentage = round(((count_change_product / total_products_count) * 100),2) if total_products_count != 0 else 0
        
        total_brands_count = Brand.objects.all().count()
        count_change_brand = Brand.objects.filter(created_at__range=[seven_days_before_datetime, current_datetime]).count()
        count_change_brand_percentage = round(((count_change_brand / total_brands_count) * 100),2) if total_brands_count != 0 else 0
        
        total_inquiries_count = Inquiry.objects.all().count()
        count_change_inquiry = Inquiry.objects.filter(created_at__range=[seven_days_before_datetime, current_datetime]).count()
        count_change_inquiry_percentage = round(((count_change_inquiry / total_inquiries_count) * 100),2) if total_inquiries_count != 0 else 0
        total_inquiry_status_count = list(Inquiry.objects.values('status').annotate(count=Count('id')))
        
        total_articles_count = Article.objects.all().count()
        count_change_article = Article.objects.filter(created_at__range=[seven_days_before_datetime, current_datetime]).count()
        count_change_article_percentage = round(((count_change_article / total_articles_count) * 100),2) if total_articles_count != 0 else 0
        
        total_jobs_count = Job.objects.all().count()
        count_change_job = Job.objects.filter(created_at__range=[seven_days_before_datetime, current_datetime]).count()
        count_change_job_percentage = round(((count_change_job / total_jobs_count) * 100),2) if total_jobs_count != 0 else 0
        
        top_five_articles = list(EntityVisit.objects.filter(entity_id=5)
                                                    .values('entity_item')
                                                    .annotate(count=Count('id'))
                                                    .annotate(
                                                        article_title=Subquery(
                                                            Article.objects.filter(id=OuterRef('entity_item'))
                                                                            .values('article_title')[:1]
                                                        )
                                                    ).order_by('-count')[:5])
        
        
        visitors_count = list(
            GeneralVisit.objects
            .values('timestamp')  # Get the raw timestamp
            .annotate(visit_count=Count('id'))
            .order_by('-timestamp')[:10]
        )

        # Process the dates after the query
        processed_visits = []
        for visit in visitors_count:
            date_str = visit['timestamp'].strftime('%Y-%m-%d')  # Format timestamp to date string
            processed_visits.append({
                'date': date_str,
                'visit_count': visit['visit_count']
            })
            
            
        processed_visits.reverse()

        # print("\nProcessed results:")
        # for visit in processed_visits:
        #     print(f"Date: {visit['date']}, Count: {visit['visit_count']}")
        
        
        
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
        
        products_visits = list(
            EntityVisit.objects
            .filter(entity_id=4, timestamp__range=[start_of_week, current_datetime])
            .values('entity_item')
            .annotate(count=Count('id'))
            .annotate(
                product_name = Subquery(
                    Product.objects.filter(id=OuterRef('entity_item'))
                                    .values('product_name')[:1]
                )
            ).order_by('-count')[:10]
        )
        
        
        brands_visits = list(
            EntityVisit.objects
            .filter(entity_id=3, timestamp__range=[start_of_week, current_datetime])
            .values('entity_item')
            .annotate(count=Count('id'))
            .annotate(
                brand_name = Subquery(
                    Brand.objects.filter(id=OuterRef('entity_item'))
                                .values('brand_name')
                )
            ).order_by('-count')[:10]
        )
    
        page_obj = {
            'total_products_count': total_products_count,
            'count_change_product': count_change_product,
            'count_change_product_percentage': count_change_product_percentage,
            'total_brands_count': total_brands_count,
            'count_change_brand': count_change_brand,
            'count_change_brand_percentage': count_change_brand_percentage,
            'total_inquiries_count': total_inquiries_count,
            'total_inquiry_status_count': total_inquiry_status_count,
            'count_change_inquiry': count_change_inquiry,
            'count_change_inquiry_percentage': count_change_inquiry_percentage,
            'total_articles_count': total_articles_count,
            'count_change_article': count_change_article,
            'count_change_article_percentage': count_change_article_percentage,
            'total_jobs_count': total_jobs_count,
            'count_change_job': count_change_job,
            'count_change_job_percentage': count_change_job_percentage,
            'top_five_articles': top_five_articles,
            'visitors_count': processed_visits,
            'products_visits': products_visits,
            'brands_visits': brands_visits
        }
        
        return JsonResponse({
            'status': True,
            'message': 'Dashboard data fetched successfully',
            'data': page_obj
        })
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': 'Error fetching dashboard data',
            'error': str(e)
        })
        
        
        