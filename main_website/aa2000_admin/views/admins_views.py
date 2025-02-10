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

from ..models import User
from ..models import Role
from ..models import UserRole
from ..models import AdminLevel
from ..models import Admin


from .logs_views import record_log, get_recent_activities




# admin  ---------------------------------------------------------------------------------------------------------------------
def admins(request):
    
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            # Get parameters for sorting, filtering, and searching
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()

            # Filter the admin list based on the search query
            admin_list = Admin.objects.select_related('level')

            if search_query:
                if filter_search_by == 'id':
                    admin_list = admin_list.filter(id__icontains=search_query)
                elif filter_search_by == 'name':
                    # Combine first and last name for searching
                    admin_list = admin_list.filter(
                        Q(admin_fname__icontains=search_query) | Q(admin_lname__icontains=search_query)
                    )
                elif filter_search_by == 'level':
                    admin_list = admin_list.filter(level__admin_level_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    admin_list = admin_list.filter(modified_at__icontains=search_query)

            # Sort the admin list based on the selected sorting option
            if sort_by == 'id-up':
                admin_list = admin_list.order_by('id')
            elif sort_by == 'id-down':
                admin_list = admin_list.order_by('-id')
            elif sort_by == 'name-up':
                admin_list = admin_list.order_by('admin_fname', 'admin_lname')  # Sort by first and last name
            elif sort_by == 'name-down':
                admin_list = admin_list.order_by('-admin_fname', '-admin_lname')  # Sort by first and last name descending
            elif sort_by == 'date-modified-up':
                admin_list = admin_list.order_by('modified_at')
            elif sort_by == 'date-modified-down':
                admin_list = admin_list.order_by('-modified_at')

            # Pagination
            # paginator = Paginator(admin_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # admin_list = paginator.get_page(page_number)

            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Admins',
                'session_admin': admin,
                'page_obj': admin_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Admin List'
            record_log(user_id, 7, 11, 0, notes)
            
            return render(request, 'aa2000_admin/admins/admins.html', page_details)
            
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    

# def search(request):
    

def add_admin(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Add New Admin',
                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            
            notes = f'Accessed Add Admin Page'
            record_log(user_id, 7, 11, 0, notes)
            
            return render(request, 'aa2000_admin/admins/add-admin.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')


def processadd_admin(request):
    
    
    adminFormData = request.POST
    fname = adminFormData.get('adminFirstName')
    lname = adminFormData.get('adminLastName')
    email = adminFormData.get('adminEmail')
    level = adminFormData.get('adminLevel')
    username = adminFormData.get('adminUsername')
    password = adminFormData.get('adminPassword')
    accessCode = adminFormData.get('adminAccessCode')
    
    # handle admin photo
    if request.FILES.get('adminImgUpload'):
        photo = request.FILES.get('adminImgUpload')
    else:
        photo = 'admins/aa2000_icon.png'
        
    
    # check first if email is already existing
    try:
        n = Admin.objects.get(admin_email=email)
        raw_data = {
            'adminFirstName': fname,
            'adminLastName': lname,
            'adminLevel': level,
            'adminEmail': email,
        }
        # return render(request, 'aa2000_admin/admins/add-admin.html', raw_data)
        return JsonResponse({
            'status': 'error',
            'type': 'Duplicate Email',
            'message': 'Email already exists',
        })
    
    # if email does not exists
    except Admin.DoesNotExist:
        
        if User.objects.filter(username=username).exists():
            
            return JsonResponse({
                'status': 'error',
                'type': 'Duplicate Username',
                'message': 'Username already exists',
                })
        
        user = User(username=username, password=password)
        user.set_password(password)
        user.save()
       
        
        admin = Admin.objects.create(
            admin_fname = fname,
            admin_lname = lname,
            admin_email = email,
            level_id = level,
            user=user,
            admin_photo = photo,
            access_code= accessCode
        )
        admin.save()
        
        admin_id = admin.id
        user_id = request.session.get('user_id')
        notes = f'Added New Admin [{admin.level.admin_level_name}] {admin.admin_fname} {admin.admin_lname}'
        record_log(user_id, 7, 1, admin_id, notes)
        
        messages.success(request, 'Admin Added Successfully')
        return JsonResponse({
            'status': 'success',
            'message': 'Admin Added Successfully',
        })


def view_admin(request, admin_id):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:
                adminData = Admin.objects.get(id=admin_id)
                adminUsername = adminData.user.username
                adminPassword = adminData.user.password
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                            'nav_title': 'View Admin',
                            'adminData': adminData,
                            'session_admin': admin,
                            'adminUsername': adminUsername,
                            'adminPassword': adminPassword,
                            'activities': get_recent_activities()
                            }
            
            notes = f'Accessed Admin Details ({adminData.admin_fname} {adminData.admin_lname})'
            admin_id = adminData.id
            record_log(user_id, 7, 2, admin_id, notes)
            
            return render(request, 'aa2000_admin/admins/view-admin.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    


def edit_admin(request, admin_id):
    
    try:
        adminData = Admin.objects.get(id=admin_id)
        adminFormData = request.POST
        adminPhoto = request.FILES.get('adminImgUpload')
        
        adminData.admin_fname = adminFormData.get('adminFirstName')
        adminData.admin_lname = adminFormData.get('adminLastName')
        adminData.admin_email = adminFormData.get('adminEmail')
        adminData.level_id = adminFormData.get('adminLevel')
        if adminPhoto:
            adminData.admin_photo = adminPhoto
        adminData.save()
        
        user_id = request.session.get('user_id')
        notes = f'Updated Admin ({adminData.admin_fname} {adminData.admin_lname} )'
        record_log(user_id, 7, 3, admin_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Admin Updated Successfully',
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Error Updating Admin',
        })
        
        
def edit_admin_credentials(request, admin_id):
    
    user_id = request.session.get('user_id')
    
    try:
        accountFormData = request.POST
        
        admin = Admin.objects.get(id=admin_id)
        user = User.objects.get(id=admin.user_id)
        
        new_password = accountFormData.get('password')
        
        user.set_password(new_password)
        user.save()
        
        notes = f'Updated Admin {admin.admin_fname} {admin.admin_lname} Account Credentials'
        record_log(user_id, 7, 3, 0, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Admin Account Credentials Updated Successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Error Updating Admin Account Credentials',
        })
        
        
def edit_admin_access_code(request, admin_id):
    
    user_id = request.session.get('user_id')
    
    try:
        accountFormData = request.POST
        
        admin = Admin.objects.get(id=admin_id)
        user = User.objects.get(id=admin.user_id)
        
        new_access_code = accountFormData.get('newCode')
        
        admin.access_code = new_access_code
        admin.save()
        
        notes = f'Updated Admin {admin.admin_fname} {admin.admin_lname} Account Access Code'
        record_log(user_id, 7, 3, 0, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Admin Account Access Code Updated Successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Error Updating Admin Account Access Code',
        })
        
       


def delete_admin(request, admin_id):
    
    user_id = request.session.get('user_id') 
    admin = Admin.objects.get(id=admin_id)
    notes = f'Deleted Admin {admin.admin_fname} {admin.admin_lname}'
    record_log(user_id, 7, 4, admin_id, notes)
    
    Admin.objects.filter(id=admin_id).delete()
    return HttpResponseRedirect(reverse('aa2000_admin:admins'))


