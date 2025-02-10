from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
import json, os
from django.views.decorators.http import require_http_methods

from ..models import User
from ..models import Role
from ..models import UserRole
from ..models import AdminLevel
from ..models import Admin
from ..models import Job
from ..models import JobDescriptions
from ..models import JobResponsibilities
from ..models import JobPreferredSkills
from ..models import JobQualifications
from ..models import JobCompensationBenefits

from .logs_views import record_log, get_recent_activities



# jobs -----------------------------------------------------------------------------------------------------------
def jobs(request):

    user_id = request.session.get('user_id')
        
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()
                
            job_list = Job.objects.all().order_by('-id')
            
            if search_query:
                if filter_search_by == 'id':
                    job_list = job_list.filter(id__icontains=search_query)
                elif filter_search_by == 'title':
                    job_list = job_list.filter(job_title__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    job_list = job_list.filter(modified_at__icontains=search_query)

            if sort_by == 'id-up':
                job_list = job_list.order_by('id')
            elif sort_by == 'id-down':
                job_list = job_list.order_by('-id')
            elif sort_by == 'title-up':
                job_list = job_list.order_by('job_title')  # Sort by first and last name
            elif sort_by == 'title-down':
                job_list = job_list.order_by('-job_title')  # Sort by first and last name descending
            elif sort_by == 'date-modified-up':
                job_list = job_list.order_by('modified_at')
            elif sort_by == 'date-modified-down':
                job_list.order_by('-modified_at')
                
            # Pagination
            # paginator = Paginator(job_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # job_list = paginator.get_page(page_number)
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Jobs',
                'session_admin': admin,
                'page_obj': job_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Jobs List'
            record_log(user_id, 6, 11, 0, notes)
                
            return render(request, 'aa2000_admin/jobs/jobs.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')

def add_job(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Add New Job',
                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            notes = f'Accessed Add Job Page'
            record_log(user_id, 6, 11, 0, notes)
            
            return render(request, 'aa2000_admin/jobs/add-job.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')



def processadd_job(request):
    try:
        if request.method != 'POST':
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method',
            }, status=405)
        
        # Get JSON data from request.POST and file from request.FILES
        job_data = request.POST
        job_image = request.FILES.get('jobImageUpload')  # Get the uploaded file

        # Check for duplicate slug
        if Job.objects.filter(job_slug=job_data.get('slug')).exists():
            return JsonResponse({
                'status': 'error',
                'error': 'Duplicate Slug',
                'message': 'Job slug already exists.'
            })
        
        # Create the job object
        job = Job.objects.create(
            job_title=job_data.get('title'),
            job_slug=job_data.get('slug'),
            job_image=job_image  # Save the uploaded file here
        )
        
        # Create job descriptions
        JobDescriptions.objects.create(
            job=job,
            short_description=job_data.get('shortDescription'),
            long_description=job_data.get('jobDescription')
        )
        
        # Create compensation and benefits
        JobCompensationBenefits.objects.create(
            job=job,
            compensation=job_data.get('compensations'),
            benefits=job_data.get('benefits')
        )
        
        # Parse JSON arrays for responsibilities, preferred skills, and qualifications
        key_responsibilities = json.loads(job_data.get('keyResponsibilities', '[]'))
        for key in key_responsibilities:
            if key.get('responsibility'):
                JobResponsibilities.objects.create(
                    job=job,
                    job_responsibility=key.get('responsibility')
                )
        
        preferred_skills = json.loads(job_data.get('preferredSkills', '[]'))
        for skill in preferred_skills:
            if skill.get('preferredSkills'):
                JobPreferredSkills.objects.create(
                    job=job,
                    job_preferred_skill=skill.get('preferredSkills')
                )
        
        qualifications = json.loads(job_data.get('qualifications', '[]'))
        for qual in qualifications:
            if qual.get('qualifications'):
                JobQualifications.objects.create(
                    job=job,
                    job_qualification=qual.get('qualifications')
                )
                
        job_id = job.id
        user_id = request.session.get('user_id')
        notes = f'Added New Job {job.job_title}'
        record_log(user_id, 6, 1, job_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Job added successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=400)



def view_job(request, slug):

    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:
                # jobData = Job.objects.get(job_slug=slug)
                # JobDescriptions = brandData.brand_details
                
                jobData = Job.objects.prefetch_related(
                    'job_responsibilities',
                    'job_qualifications',
                    'job_preferred_skills'
                ).select_related(
                    'job_description',
                    'job_compensation_benefits'
                ).get(job_slug=slug)

                # Accessing single related objects directly
                jobDescription = jobData.job_description  # Assuming a OneToOneField or ForeignKey
                jobCompensationBenefits = jobData.job_compensation_benefits  # Assuming a OneToOneField or ForeignKey

                # Accessing multiple related objects with .all()
                jobResponsibilities = jobData.job_responsibilities.all()
                jobQualifications = jobData.job_qualifications.all()
                jobPreferredSkills = jobData.job_preferred_skills.all()
                
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                            'nav_title': 'View Job',
                            'jobData': jobData,
                            'jobDescription':  jobDescription,
                            'jobResponsibilities':  jobResponsibilities,
                            'jobQualifications':  jobQualifications,
                            'jobPreferredSkills':  jobPreferredSkills,
                            'jobCompensationBenefits':  jobCompensationBenefits,
                            'session_admin': admin,
                            'activities': get_recent_activities()
                            }
            
            notes = f'Accessed Job Details ({jobData.job_title})'
            job_id = jobData.id
            record_log(user_id, 6, 2, job_id, notes)
            
            return render(request, 'aa2000_admin/jobs/view-job.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    
    
def edit_job(request, slug):
    try:
        job = Job.objects.get(job_slug=slug)
        
        job_data = request.POST
        job_image = request.FILES.get('jobImageUpload')
        
        # Check for duplicate slug if it's changed
        new_slug = job_data.get('slug')
        if new_slug != slug and Job.objects.filter(job_slug=new_slug).exists():
            return JsonResponse({
                'status': 'error',
                'error': 'Duplicate Slug'
            })
        
        job.job_title = job_data.get('title')
        job.job_slug = new_slug
        if job_image:
            job.job_image = job_image
        job.save()
        
        # Update descriptions - using the correct field name
        jobDescriptions = job.job_description
        jobDescriptions.short_description = job_data.get('shortDescription')
        jobDescriptions.long_description = job_data.get('jobDescription')
        jobDescriptions.save()
        
        # Update responsibilities - note the field name change to job_responsibility
        responsibilities_data = json.loads(job_data.get('keyResponsibilities', '[]'))
        for responsibility_data in responsibilities_data:
            if not responsibility_data.get('responsibility'):
                continue
            responsibility = JobResponsibilities.objects.get(
                id=responsibility_data['responsibility_id'],
                job=job  # Add this to ensure we're updating the correct job's responsibility
            )
            responsibility.job_responsibility = responsibility_data['responsibility']  # Changed field name
            responsibility.save()

        # Update qualifications - note the field name change to job_qualification
        qualifications_data = json.loads(job_data.get('qualifications', '[]'))
        for qualification_data in qualifications_data:
            if not qualification_data.get('qualifications'):
                continue
            qualification = JobQualifications.objects.get(
                id=qualification_data['qualifications_id'],
                job=job
            )
            qualification.job_qualification = qualification_data['qualifications']  # Changed field name
            qualification.save()

        # Update preferred skills - note the field name change to job_preferred_skill
        preferred_skills_data = json.loads(job_data.get('preferredSkills', '[]'))
        for preferred_skill_data in preferred_skills_data:
            if not preferred_skill_data.get('preferredSkills'):
                continue
            preferred_skill = JobPreferredSkills.objects.get(
                id=preferred_skill_data['preferredSkills_id'],
                job=job
            )
            preferred_skill.job_preferred_skill = preferred_skill_data['preferredSkills']  # Changed field name
            preferred_skill.save()

        # Update compensations and benefits - note the field name changes
        jobCompensationBenefits = job.job_compensation_benefits
        jobCompensationBenefits.compensation = job_data.get('compensations')  # Changed to match model field
        jobCompensationBenefits.benefits = job_data.get('benefits')
        jobCompensationBenefits.save()

        job_id = job.id
        user_id = request.session.get('user_id')
        notes = f'Updated Job ({job.job_title})'
        record_log(user_id, 6, 3, job_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'slug':  job.job_slug,
            'message': 'Job updated successfully',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
        
        
def delete_job(request, slug):
    try:
        job = Job.objects.get(job_slug=slug)
        jobCompensationBenefits = JobCompensationBenefits.objects.filter(job=job)
        jobPreferredSkills = JobPreferredSkills.objects.filter(job=job)
        jobQualifications = JobQualifications.objects.filter(job=job)
        jobResponsibilities = JobResponsibilities.objects.filter(job=job)
        jobDescriptions = JobDescriptions.objects.filter(job=job)
        
        user_id = request.session.get('user_id') 
        job_id = job.id
        notes = f'Deleted Job {job.job_title}'
        record_log(user_id, 6, 4, job_id, notes)
            
        if job.job_image:
            delete_file(job.job_image.path)
            
        jobCompensationBenefits.delete()
        jobPreferredSkills.delete()
        jobQualifications.delete()
        jobResponsibilities.delete()
        jobDescriptions.delete()
        job.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Job deleted successfully',
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred: {}'.format(str(e))
        }, status=500)
        

def delete_file(file_path):
    """Helper function to delete a file from the filesystem."""
    if os.path.isfile(file_path):
        os.remove(file_path)
        