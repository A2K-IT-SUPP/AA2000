from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt

from ..models import User
from ..models import Role
from ..models import UserRole
from ..models import AdminLevel
from ..models import Admin
from ..models import System
from ..models import Brand
from ..models import BrandDetail

from .logs_views import record_log, get_recent_activities


# brands ----------------------------------------------------------------------------------------------------------------
def brands(request):
    
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()
            
            brand_list = Brand.objects.select_related('system')
            
            if search_query:
                if filter_search_by == 'id':
                    brand_list = brand_list.filter(id__icontains=search_query)
                elif filter_search_by == 'name':
                    brand_list = brand_list.filter(brand_name__icontains=search_query)
                elif filter_search_by == 'level':
                    brand_list = brand_list.filter(system__system_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    brand_list = brand_list.filter(modified_at__icontains=search_query)

            if sort_by == 'id-up':
                brand_list = brand_list.order_by('id')
            elif sort_by == 'id-down':
                brand_list = brand_list.order_by('-id')
            elif sort_by == 'name-up':
                brand_list = brand_list.order_by('brand_name')  # Sort by first and last name
            elif sort_by == 'name-down':
                brand_list = brand_list.order_by('-brand_name')  # Sort by first and last name descending
            elif sort_by == 'date-modified-up':
                brand_list = brand_list.order_by('modified_at')
            elif sort_by == 'date-modified-down':
                brand_list = brand_list.order_by('-modified_at')
                
            # Pagination
            # paginator = Paginator(brand_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # brand_list = paginator.get_page(page_number)
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Brands',
                'session_admin': admin,
                'page_obj': brand_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Brands List'
            record_log(user_id, 3, 11, 0, notes)
            
            return render(request, 'aa2000_admin/brands/brands.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    

def add_brand(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Add New Brand',
                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            
            notes = f'Accessed Add Brand Page'
            record_log(user_id, 3, 11, 0, notes)
            
            return render(request, 'aa2000_admin/brands/add-brand.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    
    
def processadd_brand(request):
    name = request.POST.get('brandName')
    slug = request.POST.get('brandSlug')
    system = request.POST.get('brandSystem')
    description_1 = request.POST.get('brandDescription_1')
    description_2 = request.POST.get('brandDescription_2')
    
    other_description = request.POST.get('brandOtherDescription')

    logo = request.FILES.get('brandLogoUpload', 'brands/aa2000_icon.png')
    brand_img_1 = request.FILES.get('brandDescImg1Upload', None)
    brand_img_2 = request.FILES.get('brandDescImg2Upload', None)
        
    try:
        n = Brand.objects.get(brand_slug=slug)
        raw_data = {
            'brand_name': name,
            'slug': slug,
            'system': system,
            'logo': logo,
            'brandOtherDescription': other_description
        }
        

        return render(request, 'aa2000_admin/brands/add-brand.html', raw_data)
    except Brand.DoesNotExist:
        brand = Brand.objects.create(
            brand_name=name,
            brand_slug=slug,
            
            system_id=system,
            brand_logo=logo,
        )
        brand.save()
        
        brandDetail = BrandDetail.objects.create(
            brand=brand,
            brand_description_1=description_1,
            brand_description_2=description_2,
            brand_image_1=brand_img_1,
            brand_image_2=brand_img_2,
            other_details=other_description
        )
        brandDetail.save()
        
        brand_id = brand.id
        user_id = request.session.get('user_id')
        notes = f'Added New Brand {brand.brand_name}'
        record_log(user_id, 3, 1, brand_id, notes)
        
        return HttpResponseRedirect('/admin/brands')
    

def view_brand(request, slug):

    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:
                brandData = Brand.objects.get(brand_slug=slug)
                brandDetails = brandData.brand_details
                
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                            'nav_title': 'View Brand',
                            'brandData': brandData,
                            'brandDetails':  brandDetails,
                            'session_admin': admin,
                            'activities': get_recent_activities()
                            }
            
            notes = f'Accessed Brand Details ({brandData.brand_name})'
            brand_id = brandData.id
            record_log(user_id, 3, 2, brand_id, notes)
            
            return render(request, 'aa2000_admin/brands/view-brand.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')

def edit_brand(request, slug):
    brand = get_object_or_404(Brand, brand_slug=slug)
    current_time = timezone.now()
    page_details = {
        'current_time': current_time,
        'nav_title': 'View Admin',
        'brandData': brand,
    }
    
    try:
        # Retrieve form data
        name = request.POST.get('brandName')
        new_slug = request.POST.get('brandSlug')
        system = request.POST.get('brandSystem')
        description_1 = request.POST.get('brandDescription_1')
        description_2 = request.POST.get('brandDescription_2')
        logo = request.FILES.get('brandLogoUpload')
        brand_img_1 = request.FILES.get('brandDescImg1Upload')
        brand_img_2 = request.FILES.get('brandDescImg2Upload')
        other_description = request.POST.get('brandOtherDescription')

    except (KeyError, Brand.DoesNotExist) as e:
        messages.error(request, f'Error updating brand: {str(e)}')
        return render(request, 'aa2000_admin/brands/view-brand.html', page_details)
    else:
        brandData = Brand.objects.get(brand_slug=slug)
        brandData.brand_name = name
        brandData.brand_slug = new_slug
        brandData.system_id = system
        if logo:
            brandData.brand_logo = logo
        brandData.save()

        # Update brand details
        brandDetails = brandData.brand_details  # assuming brand_details is a OneToOneField
        brandDetails.brand_description_1 = description_1
        brandDetails.brand_description_2 = description_2
        brandDetails.other_details = other_description
        if brand_img_1:
            brandDetails.brand_image_1 = brand_img_1
        if brand_img_2:
            brandDetails.brand_image_2 = brand_img_2

        brandDetails.save()
        
        brand_id = brand.id
        user_id = request.session.get('user_id')
        notes = f'Updated Brand ({brand.brand_name})'
        record_log(user_id, 3, 3, brand_id, notes)
        
                # Redirect to the view page with updated slug
        return HttpResponseRedirect(reverse('aa2000_admin:view_brand', args=(new_slug,)))


def delete_brand(request, slug):
    
    user_id = request.session.get('user_id') 
    brand = Brand.objects.get(brand_slug=slug)
    brand_id = brand.id
    notes = f'Deleted Brand {brand.brand_name}'
    record_log(user_id, 3, 4, brand_id, notes)
    
    Brand.objects.filter(brand_slug=slug).delete()
    return HttpResponseRedirect(reverse('aa2000_admin:brands'))

