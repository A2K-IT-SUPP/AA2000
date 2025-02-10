from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
from ..models import AdminActivityLogs






# logs -----------------------------------------------------------------------------------------------------------
def logs(request): 
    user_id = request.session.get('user_id')
        
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()
                
            # article_list = Article.objects.all().order_by('-id')
            log_lists = AdminActivityLogs.objects.select_related(
                'admin',     
                'admin__user',
                'admin__level',
                'action',    
                'entity'      
            ).all().order_by('-id')
            
            if search_query:
                if filter_search_by == 'id':
                    log_lists = log_lists.filter(id__icontains=search_query)
                elif filter_search_by == 'level':
                    log_lists = log_lists.filter(admin_on_activity__admin_level__icontains=search_query)
                elif filter_search_by == 'action':
                    log_lists = log_lists.filter(activity_action__action_name__icontains=search_query)
                elif filter_search_by == 'entity':
                    log_lists = log_lists.filter(activity_entity__entity_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    log_lists = log_lists.filter(modified_at__icontains=search_query)

                
            # Pagination
            # paginator = Paginator(log_lists, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # log_lists = paginator.get_page(page_number)
            
            paginator = Paginator(log_lists, 10)

            page_number = request.GET.get('page')

            try:
                log_lists = paginator.get_page(page_number)
            except PageNotAnInteger:
                log_lists = paginator.get_page(1)
            except EmptyPage:
                log_lists = paginator.get_page(paginator.num_pages)
                
            page_range = paginator.page_range
            current_page = log_lists.number
            
            page_range_start = max(current_page - 2, 1)
            page_range_end = min(current_page + 2, paginator.num_pages)
            
            page_range = page_range[page_range_start - 1:page_range_end]
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Activity Logs',
                'session_admin': admin,
                'page_obj': log_lists,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities().filter,
                'log_lists': log_lists,
                'page_range': page_range,
            }
                
            notes = f'Accessed Articles List'
            record_log(user_id, 5, 11, 0, notes)
            
            return render(request, 'aa2000_admin/logs.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')


def record_log(user_id, entity_id, action_id, entity_item, notes):
    
    user = User.objects.get(id=user_id)
    admin = Admin.objects.get(user=user)
    
    if user_id and action_id and entity_id:
        AdminActivityLogs.objects.create(
            admin=admin,
            action_id=action_id,
            entity_id=entity_id,
            entity_item=entity_item,
            notes=notes
        )
    


def get_recent_activities():
    
    log_lists = AdminActivityLogs.objects.select_related(
    'admin',
    'admin__user',
    'admin__level',
    'action',
    'entity'
    ).all().order_by('-id')[:15]
    
    return log_lists