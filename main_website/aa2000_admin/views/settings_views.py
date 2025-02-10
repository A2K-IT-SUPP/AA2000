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

from .logs_views import record_log, get_recent_activities


# settings --------------------------------------------------------------------------------------------------------------
def admin_settings(request):

    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                            'nav_title': 'Settings',
                            'session_admin': admin,
                            'user_admin':  user,
                            'activities': get_recent_activities()
                            }
            notes = f'Accessed the Settings Page'
            record_log(user_id, 9, 2, 0, notes)
            return render(request, 'aa2000_admin/settings.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    
    
def edit_admin_settings(request):
    
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            access_code = admin.access_code
            accountData = request.POST
            adminPhoto = request.FILES.get('admin_photo')
            
            
            # compare the access code of the admin
            req_access_code = accountData.get('access_code')
            if req_access_code != access_code:
                return JsonResponse({
                    'status': 'error',
                    'type': 'Security Code',
                    'message': 'Invalid access code.'
                })
                        
            adminData = Admin.objects.get(user_id=user_id)
            adminData.admin_fname = accountData.get('admin_fname')
            adminData.admin_lname = accountData.get('admin_lname')
            adminData.admin_email = accountData.get('admin_email')
            if adminPhoto:
                adminData.admin_photo = adminPhoto  
            adminData.save()
            
            notes = f'Updated Account Details'
            record_log(user_id, 9, 3, 0, notes)
            return JsonResponse({
                'status': 'success',
                'type': 'Account Update',
                'message': 'Admin settings updated successfully.'
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'type': 'Database',
                'message': str(e)
                }, status=400)
            
            
def edit_credentials_admin_settings(request):
    
    user_id = request.session.get('user_id')
                
    # prepare the request data
    accountData = request.POST

    if user_id and accountData.get('isChangePass') == '1':
        try:
            user = User.objects.get(id=user_id)
            admin = Admin.objects.get(user=user)

            # check first if the old password is correct
            old_password = accountData.get('oldPassword')
            
            if user.check_password(old_password):
                # check if the new password is the same as the old password
                new_password = accountData.get('newPassword')
                if new_password == old_password:
                    return JsonResponse({
                        'status': 'error',
                        'type': 'Password Update',
                        'message': 'New password cannot be the same as the old password.'
                        })
                
                user.set_password(accountData.get('newPassword'))
                user.save()
                            
                notes = f'Updated Account Credentials'
                record_log(user_id, 9, 3, 0, notes)
                return JsonResponse({
                    'status': 'success',
                    'type': 'Account Update',
                    'message': 'Admin credentials updated successfully.'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'type': 'Password Update',
                    'message': 'Old password is incorrect.'
                    })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'type': 'Database',
                'message': str(e)
                }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'type': 'Authentication',
            'message': 'You are not authorized to perform this action.'
            })
            

def edit_access_code_admin_settings(request):
    user_id = request.session.get('user_id')
    
    accountData = request.POST
    
    if user_id and accountData.get('isChangeCode') == '1':
        try:
            user = User.objects.get(id=user_id)
            admin = Admin.objects.get(user=user)
            
            old_access_code = accountData.get('oldCode')
            current_access_code = admin.access_code
            
            if old_access_code == current_access_code:
                new_access_code = accountData.get('newCode')
                
                if old_access_code == new_access_code:
                    return JsonResponse({
                        'status': 'error',
                        'type': 'Access Code Update',
                        'message': 'New access code is the same as the old one.'
                    })
                
                admin.access_code = new_access_code
                admin.save()
                
                notes = f'Updated Account Access Code                                                                                                                                  '
                record_log(user_id, 9, 3, 0, notes)
                return JsonResponse({
                    'status': 'success',
                    'type': 'Access Code Update',
                    'message': 'Access code has been updated successfully.'
                })
                
            else:
                return JsonResponse({
                    'status': 'error',
                    'type': 'Access Code Update',
                    'message': 'Old access code is incorrect.'
                    })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'type': 'Database',
                'message': 'An error occurred while updating access code.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'type': 'Access Code Update',
            'message': 'You are not authorized to update access code.'
            })