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

from ..models import InquiryConcernCategory
from ..models import Inquiry
from ..models import InquiryDetails
from ..models import Rfq
from ..models import InquiryReply
from ..models import InquiryReplyAttachments

from .logs_views import record_log, get_recent_activities
from ..email_utils import send_custom_email

# inquiries------------------------------------------------------------------------------------------------
def inquiries(request):
    user_id = request.session.get('user_id')
        
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()
                
            inquiry_list = Inquiry.objects.select_related(
                'inquiry_details__inquiry_rfq',
                'inquiry_details__concern_category'
            ).all().order_by('-id')

            # Filter logic
            if search_query:
                if filter_search_by == 'name':
                    inquiry_list = inquiry_list.filter(
                        Q(inquiry_details__fname__icontains=search_query) |
                        Q(inquiry_details__lname__icontains=search_query)
                    )
                elif filter_search_by == 'status':
                    inquiry_list = inquiry_list.filter(status__icontains=search_query)
                elif filter_search_by == 'concern':
                    inquiry_list = inquiry_list.filter(inquiry_details__concern_category__concern_category_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    inquiry_list = inquiry_list.filter(modified_at__icontains=search_query)

            # Sorting logic
            if sort_by == 'date-up':
                inquiry_list = inquiry_list.order_by('modified_at')
            elif sort_by == 'date-down':
                inquiry_list = inquiry_list.order_by('-modified_at')
                
            # Pagination
            # paginator = Paginator(inquiry_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # inquiry_list = paginator.get_page(page_number)
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Inquiries',
                'session_admin': admin,
                'page_obj': inquiry_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
                
            notes = f'Accessed Inquiries'
            record_log(user_id, 2, 11, 0, notes)
            
            return render(request, 'aa2000_admin/inquiries/inquiries.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')


def view_inquiry(request, slug):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:

                inquiry = Inquiry.objects.select_related(
                    'inquiry_details__inquiry_rfq',
                    'inquiry_details__concern_category'
                ).get(ticket=slug)
                
                
                if inquiry.status != 'DONE':
                    inquiry.status = 'PENDING'
                    inquiry.save()
                
                inquiry_details = inquiry.inquiry_details
                rfq = inquiry_details.inquiry_rfq if hasattr(inquiry_details, 'inquiry_rfq') else None

                replies = InquiryReply.objects.filter(inquiry_id=inquiry.id).prefetch_related('inquiry_reply_attachment')

                
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'View Inquiry',
                'inquiry': inquiry,
                'inquiry_details': inquiry_details, 
                'rfq': rfq,
                'replies': replies,
                'session_admin': admin,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Inquiry Details ({inquiry.ticket})'
            inquiry_id = inquiry.id
            record_log(user_id, 2, 2, inquiry_id, notes)
            
            return render(request, 'aa2000_admin/inquiries/view-inquiry.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')



def reply_inquiry(request, slug):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)  
        admin = Admin.objects.get(user=user)  
        
        replyData = request.POST
        inquiry = Inquiry.objects.get(ticket=slug)
        inquiry_details = inquiry.inquiry_details
        reply_text = replyData.get('reply')
        files = request.FILES.getlist('files[]')
        
        
        has_files = 1 if files else 0
        
        inquiry_reply = InquiryReply.objects.create(
            inquiry=inquiry,
            reply=reply_text,
            admin_id=admin.id,
            hasFile=has_files,
        )
        
        inquiry.status='DONE'
        inquiry.save()
        
        for file in files:
            attachment = InquiryReplyAttachments.objects.create(
                inquiry_reply=inquiry_reply,
                inquiry_attachment=file
            )
            attachment.save()
            
        send_custom_email(
            user=inquiry_details,
            email_type='admin_reply',
            ticket_id=inquiry.ticket,
            reply_message=reply_text,
            attachments=files
        )
        
        notes = f'Replied to an Inquiry ({inquiry.ticket})'
        inquiry_id = inquiry.id
        record_log(user_id, 2, 11, inquiry_id, notes)
            
        return JsonResponse({
            'status': 'success',
            'message': 'Reply sent successfully.',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })
        
        
        
