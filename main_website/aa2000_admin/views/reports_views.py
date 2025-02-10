from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, OuterRef, Subquery, Min
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear, ExtractYear, ExtractMonth, ExtractWeek, ExtractDay, Lower
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
from django.db import models
import json, calendar
from calendar import monthcalendar 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

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



# reports --------------------------------------------------------------------------------------------------
def reports(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user) 
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Reports',

                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            return render(request, 'aa2000_admin/reports.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')



def get_top_products(time_period='today'):
    current_datetime = timezone.now()
    
    # Define time ranges
    time_filters = {
        'today': current_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
        'week': current_datetime - timedelta(days=current_datetime.weekday()),
        'month': current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        'year': current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    }
    
    start_date = time_filters.get(time_period)
    
    return list(EntityVisit.objects
        .filter(
            entity_id=4,
            timestamp__gte=start_date,
            timestamp__lte=current_datetime
        )
        .values('entity_item')
        .annotate(
            count=Count('id'),
            product_name=Subquery(
                Product.objects.filter(
                    id=OuterRef('entity_item')
                ).values('product_name')[:1]
            )
        )
        .order_by('-count')[:10]
    )


def reports_get_products_data(request):
    try:
        
        current_datetime = timezone.now()
        
        total_products_count = Product.objects.all().count()
        per_system_count = list(Product.objects.values('system_id')
                                                .annotate(
                                                    count=Count('id'))
                                                .annotate(
                                                    system_name=Subquery(
                                                        System.objects.filter(id=OuterRef('system_id'))
                                                                        .values('system_name')[:1])
                                                ).order_by('-count'))
        
        per_system_category_count = Product.objects.values('system_id', 'category_id') \
            .annotate(count=Count('id')) \
            .annotate(
                system_name=Subquery(
                    System.objects.filter(id=OuterRef('system_id'))
                    .values('system_name')[:1]
                ),
                category_name=Subquery(
                    ProductCategory.objects.filter(id=OuterRef('category_id'))
                    .values('category_name')[:1]
                )
            )
            
        productSystemCategoryCount = {}
        
        for item in per_system_category_count:
            system_name = item['system_name']
            category_name = item['category_name']
            count = item['count']
            
            if system_name not in productSystemCategoryCount:
                productSystemCategoryCount[system_name] = {
                    'system_name': system_name,
                    'categories': []
                }
                
            productSystemCategoryCount[system_name]['categories'].append({
                'category_name': category_name,
                'count': count
            })
                
        
        rankings = {
            'daily_top_products': get_top_products('today'),
            'weekly_top_products': get_top_products('week'),
            'monthly_top_products': get_top_products('month'),
            'yearly_top_products': get_top_products('year')
        }
        
        
        # recent_products_added = Product.objects.all().order_by('-created_at')[:10]
        product_recently_added = list(Product.objects.order_by('-created_at')[:10]
                                      .values('product_name', 'created_at')
                                      .annotate(system_name=Subquery(System.objects.filter(id=OuterRef('system_id')).values
                                                                     ('system_name')[:1])))
        
        
        data = {
            'total_products_count': total_products_count,
            'per_system_count': per_system_count,
            'per_system_category_count': productSystemCategoryCount,
            'top_viewed_products_day': rankings['daily_top_products'],
            'top_viewed_products_week': rankings['weekly_top_products'],
            'top_viewed_products_month': rankings['monthly_top_products'],
            'top_viewed_products_year': rankings['yearly_top_products'],
            'product_recently_added': product_recently_added
        }
        
        return JsonResponse({
            'data': data,
            'status': 'success',
            'message': 'Data retrieved successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })
        
        
        
        
def get_top_brands(time_period='today'):
    current_datetime = timezone.now()
    
    # Define time ranges
    time_filters = {
        'today': current_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
        'week': current_datetime - timedelta(days=current_datetime.weekday()),
        'month': current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
        'year': current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    }
    
    start_date = time_filters.get(time_period)
    
    return list(EntityVisit.objects
        .filter(
            entity_id=3,
            timestamp__gte=start_date,
            timestamp__lte=current_datetime
        )
        .values('entity_item')
        .annotate(
            count=Count('id'),
            brand_name=Subquery(
                Brand.objects.filter(
                    id=OuterRef('entity_item')
                ).values('brand_name')[:1]
            )
        )
        .order_by('-count')[:10]
    )
        
def reports_get_brands_data(request):
    try:
        current_datetime = timezone.now()
        
        total_brands_count = Brand.objects.all().count()
        per_system_count = list(Brand.objects.values('system_id')
                                                .annotate(
                                                    count=Count('id'))
                                                .annotate(
                                                    system_name=Subquery(
                                                        System.objects.filter(id=OuterRef('system_id'))
                                                                        .values('system_name')[:1])
                                                ).order_by('-count'))
                
        
        rankings = {
            'daily_top_brands': get_top_brands('today'),
            'weekly_top_brands': get_top_brands('week'),
            'monthly_top_brands': get_top_brands('month'),
            'yearly_top_brands': get_top_brands('year')
        }
        
        
        brand_recently_added = list(Brand.objects.order_by('-created_at')[:10]
                                      .values('brand_name', 'created_at')
                                      .annotate(system_name=Subquery(System.objects.filter(id=OuterRef('system_id')).values
                                                                     ('system_name')[:1])))
        
        
        data = {
            'total_brands_count': total_brands_count,
            'per_system_count': per_system_count,
            'top_viewed_brands_day': rankings['daily_top_brands'],
            'top_viewed_brands_week': rankings['weekly_top_brands'],
            'top_viewed_brands_month': rankings['monthly_top_brands'],
            'top_viewed_brands_year': rankings['yearly_top_brands'],
            'brand_recently_added': brand_recently_added
        }
        
        return JsonResponse({
            'data': data,
            'status': 'success',
            'message': 'Data retrieved successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })
        

def get_inquiry_analytics() -> Dict[str, List[Dict[str, Any]]]:
    try:
        current_datetime = timezone.now()
        
        # Daily analytics (last 7 days)
        seven_days_ago = current_datetime - timedelta(days=6)
        # print(f"Fetching daily data from: {seven_days_ago.date()} to {current_datetime.date()}")  # Debug
        # Fetch all inquiries in the range
        inquiries = Inquiry.objects.filter(
            created_at__gte=seven_days_ago,
            created_at__lte=current_datetime
        )

        # Debug print
        # print(f"Query: {inquiries.query}")
        # print(f"Total records fetched: {inquiries.count()}")

        # Group inquiries by date
        daily_counts = defaultdict(int)
        for inquiry in inquiries:
            day = inquiry.created_at.date()  # Extract the date part of created_at
            daily_counts[day] += 1

        # Format the result
        formatted_inquiries_per_day = [
            {
                "day": day.strftime("%B %d, %Y"),
                "count": count
            }
            for day, count in sorted(daily_counts.items())
        ]

        # Debug print
        # print(f"Formatted inquiries: {formatted_inquiries_per_day}")


        # Weekly analytics (last 4 weeks)
        four_weeks_ago = current_datetime - timedelta(weeks=4)
        # print(f"Fetching weekly data from: {four_weeks_ago.date()} to {current_datetime.date()}")  # Debug

        # Fetch all inquiries in the range
        inquiries = Inquiry.objects.filter(
            created_at__gte=four_weeks_ago,
            created_at__lte=current_datetime
        )

        # Debug print
        # print(f"Query: {inquiries.query}")
        # print(f"Total records fetched: {inquiries.count()}")

        # Group inquiries by week start date
        weekly_counts = defaultdict(int)
        for inquiry in inquiries:
            # Calculate the start of the week (Monday)
            week_start = inquiry.created_at - timedelta(days=inquiry.created_at.weekday())
            week_start = week_start.date()  # Convert to date
            weekly_counts[week_start] += 1

        # Format the result
        formatted_inquiries_per_week = [
            {
                "week": f"Week starting {week_start.strftime('%B %d, %Y')}",
                "count": count
            }
            for week_start, count in sorted(weekly_counts.items())
        ]

        # Debug print
        # print(f"Formatted weekly inquiries: {formatted_inquiries_per_week}")
        
        monthly_inquiries = (
            Inquiry.objects.filter(
                created_at__year=current_datetime.year
            )
            .extra({
                'month': "MONTH(created_at)"
            })
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        
        # Debug print
        # print(f"Monthly query: {monthly_inquiries.query}")
        # print(f"Monthly records found: {monthly_inquiries.count()}")

        formatted_inquiries_per_month = [
            {
                "month": calendar.month_name[entry['month']],
                "count": entry['count']
            }
            for entry in monthly_inquiries
        ]

        # Yearly analytics (all time)
        # print("Fetching yearly data")  # Debug
        
        yearly_inquiries = (
            Inquiry.objects.all()
            .extra({
                'year': "YEAR(created_at)"
            })
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        
        # Debug print
        # print(f"Yearly query: {yearly_inquiries.query}")
        # print(f"Yearly records found: {yearly_inquiries.count()}")

        formatted_inquiries_per_year = [
            {
                "year": str(entry['year']),
                "count": entry['count']
            }
            for entry in yearly_inquiries
        ]

        # Handle empty results by providing default values
        if not formatted_inquiries_per_day:
            print("No daily data found, creating default values")  # Debug
            for i in range(7):
                date = current_datetime - timedelta(days=i)
                formatted_inquiries_per_day.append({
                    "day": date.strftime("%B %d, %Y"),
                    "count": 0
                })
            formatted_inquiries_per_day.reverse()

        if not formatted_inquiries_per_week:
            print("No weekly data found, creating default values")  # Debug
            for i in range(4):
                week_start = current_datetime - timedelta(weeks=i)
                week_number = int(week_start.strftime('%U'))
                suffix = 'th' if 11 <= week_number <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(week_number % 10, 'th')
                formatted_inquiries_per_week.append({
                    "week": f"{week_number}{suffix} Week of {week_start.strftime('%B')}",
                    "count": 0
                })
            formatted_inquiries_per_week.reverse()

        if not formatted_inquiries_per_month:
            print("No monthly data found, creating default value")  # Debug
            current_month = current_datetime.strftime("%B")
            formatted_inquiries_per_month.append({
                "month": current_month,
                "count": 0
            })

        if not formatted_inquiries_per_year:
            print("No yearly data found, creating default value")  # Debug
            current_year = current_datetime.strftime("%Y")
            formatted_inquiries_per_year.append({
                "year": current_year,
                "count": 0
            })

        return {
            'daily': formatted_inquiries_per_day,
            'weekly': formatted_inquiries_per_week,
            'monthly': formatted_inquiries_per_month,
            'yearly': formatted_inquiries_per_year,
            'status': 'success'
        }

    except Exception as e:
        print(f"Error in get_inquiry_analytics: {str(e)}")  # Debug print for errors
        return {
            'daily': [],
            'weekly': [],
            'monthly': [],
            'yearly': [],
            'status': 'error',
            'message': str(e)
        }

def reports_get_inquiries_data(request):
    try:
        
        current_datetime = timezone.now()
        
        total_inquiries_count = Inquiry.objects.all().count()
        per_inquiry_status_count = list(Inquiry.objects.values('status')
                                                    .annotate(count=Count('id')))
        per_inquiry_status_concern = list(InquiryDetails.objects.values('concern_category')
                                                        .annotate(count=Count('id'))
                                                        .annotate(concern_category_name=Subquery(
                                                            InquiryConcernCategory.objects.filter(id=OuterRef('concern_category'))
                                                                                        .values('concern_category_name')[:1]
                                                        ))
                                        )

        
        resultCount = get_inquiry_analytics()
        
        if resultCount['status'] == 'error':
            print(f"Error: {resultCount.get('message')}")
        else:
            # Access the data
            formatted_inquiries_per_day = resultCount['daily']
            formatted_inquiries_per_week = resultCount['weekly']
            formatted_inquiries_per_month = resultCount['monthly']
            formatted_inquiries_per_year = resultCount['yearly']
            
        # if resultCount['status'] == 'success':
        #     print(f"Daily entries: {len(resultCount['daily'])}")
        #     print(f"Weekly entries: {len(resultCount['weekly'])}")
        #     print(f"Monthly entries: {len(resultCount['monthly'])}")
        #     print(f"Yearly entries: {len(resultCount['yearly'])}")
        # else:
        #     print(f"Error: {resultCount.get('message')}")
        
        
        
            
        page_obj = {
            "total_inquiries_count": total_inquiries_count,
            "per_inquiry_status_count": per_inquiry_status_count,
            "per_inquiry_status_concern": per_inquiry_status_concern,
            "inquiries_per_day": formatted_inquiries_per_day,
            "inquiries_per_week": formatted_inquiries_per_week,
            "inquiries_per_month": formatted_inquiries_per_month,
            "inquiries_per_year": formatted_inquiries_per_year,
        }
        
        return JsonResponse({
            "data": page_obj,
            "status": "success",
            'message': 'Data retrieved successfully',
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    
    
def reports_get_articles_data(request):
    try: 
        current_datetime = timezone.now()
        
        total_articles_count = Article.objects.all().count()
        per_article_keyword = list(
            Article.objects.annotate(lower_keywords=Lower('keywords'))
                            .values('lower_keywords')
                            .annotate(count=Count('id'))
                            .order_by('-count')
        )
        
        top_ten_articles = list(EntityVisit.objects.filter(entity_id=5)
                                                    .values('entity_item')
                                                    .annotate(count=Count('id'))
                                                    .values('count')
                                                    .annotate(
                                                        article_title=Subquery(
                                                            Article.objects.filter(id=OuterRef('entity_item'))
                                                                            .values('article_title')[:1]
                                                        ),
                                                        article_author=Subquery(
                                                            Author.objects.filter(article_id=OuterRef('entity_item'))
                                                                        .values('author_name')[:1]
                                                        )
                                                    ).order_by('-count')[:10])
        
        
        page_obj = {
            "total_articles_count": total_articles_count,
            "per_article_keyword": per_article_keyword,
            "top_ten_articles": top_ten_articles,
        }
        
        
        return JsonResponse({
            "data": page_obj,
            "status": "success",
            'message': 'Data retrieved successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })