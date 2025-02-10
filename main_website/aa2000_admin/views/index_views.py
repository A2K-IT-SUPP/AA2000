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

from .logs_views import record_log


# login session -----------------------------------------------------------------------------------------------
def index(request):
    # Check if the user is already authenticated by looking for 'user_id' in the session
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            # Retrieve the User and Admin instances
            user = User.objects.get(id=user_id)
            admin = Admin.objects.get(user=user)

            # Prepare page details
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Dashboard',
                'session_admin': admin,
            }
            
            # Render the home page with the user's session details
            return render(request, 'aa2000_admin/home.html', page_details)
        
        except (User.DoesNotExist, Admin.DoesNotExist):
            # If there's an issue retrieving user or admin, redirect to login page
            return redirect('aa2000_admin:login')
    
    # If no user session, render the login page
    return render(request, 'aa2000_admin/index.html')

# temporary login  method

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)  # Get the user from the database
#         except User.DoesNotExist:
#             messages.error(request, 'Login Failed. Please check your username and password.')
#             return render(request, 'aa2000_admin/index.html')  # Render the login page again

#         if user.check_password(password):  # Use the custom check_password method
#             # Here, you should also use Django's session management to log the user in
#             # For example, you can set the session manually if you want to keep it simple
#             request.session['user_id'] = user.id  # Store user ID in the session
#             user_id = request.session.get('user_id')
#             notes = f'Logged In'
#             record_log(user_id, 1, 7, 0, notes)
            
#             return HttpResponseRedirect('/admin/home')  # Redirect to the admin home
#         else:
#             messages.error(request, 'Login Failed. Please check your username and password.')

#     return render(request, 'aa2000_admin/index.html')  # Render the login page if login fails


def login(request):
    loginFormData = request.POST
    loginPhase = loginFormData.get('login_phase')

    if loginPhase == 'credentials':
        username = loginFormData.get('username')
        password = loginFormData.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Store username in session for use in the accessCode phase
                request.session['username'] = username
                return JsonResponse({
                    'status': 'success',
                    'username': user.username,
                    'nextPhase': 'accessCode',
                    'message': 'Login Credentials Successful'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'nextPhase': 'credentials',
                    'message': 'Invalid Password'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'nextPhase': 'credentials',
                'message': 'Invalid Username'
            })

    elif loginPhase == 'accessCode':
        username = request.session.get('username')
        if not username:
            return JsonResponse({
                'status': 'error',
                'nextPhase': 'credentials',
                'message': 'Session expired. Please log in again.'
            })
        
        user = User.objects.get(username=username)
        try:
            admin = Admin.objects.get(user=user)
            storedAccessCode = admin.access_code
            loginAccessCode = loginFormData.get('accessCode')
            
            if storedAccessCode == loginAccessCode:
                request.session['user_id'] = user.id
                user_id = request.session.get('user_id')
                notes = f'Logged In'
                record_log(user_id, 1, 7, 0, notes)
                
                return JsonResponse({
                    'status': 'success',
                    'nextPhase': 'dashboard',
                    'message': 'Access Code Successful'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'nextPhase': 'accessCode',
                    'message': 'Invalid Access Code'
                })
        except Admin.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'nextPhase': 'credentials',
                'message': 'Admin record not found. Please contact support.'
            })

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid login phase'
        })
                
    
    
    

def logout(request):

    # Check if the user is already authenticated by looking for 'user_id' in the session
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user_id = request.session.get('user_id')
            notes = f'Logged Out'
            record_log(user_id, 1, 8, 0, notes)        
            request.session.flush()  # Clear all session data
            messages.success(request, 'You have been logged out.')
            return render(request, 'aa2000_admin/index.html')
        
        except (User.DoesNotExist, Admin.DoesNotExist):
            # If there's an issue retrieving user or admin, redirect to login page
            return redirect('aa2000_admin:login')
    
    # If no user session, render the login page
    return render(request, 'aa2000_admin/index.html')