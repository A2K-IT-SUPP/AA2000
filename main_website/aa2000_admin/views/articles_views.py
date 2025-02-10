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
from ..models import Article
from ..models import ArticleContent
from ..models import Author

from .logs_views import record_log, get_recent_activities



# articles ------------------------------------------------------------------------------------------------------------
def articles(request):

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
            article_list = Article.objects.select_related('article_author').all()
            
            # Filter logic
            if search_query:
                if filter_search_by == 'id':
                    article_list = article_list.filter(id__icontains=search_query)
                elif filter_search_by == 'title':
                    article_list = article_list.filter(article_title__icontains=search_query)
                elif filter_search_by == 'author':
                    article_list = article_list.filter(article_author__author_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    article_list = article_list.filter(modified_at__icontains=search_query)

            # Sorting logic
            if sort_by == 'id-up':
                article_list = article_list.order_by('id')
            elif sort_by == 'id-down':
                article_list = article_list.order_by('-id')
            elif sort_by == 'title-up':
                article_list = article_list.order_by('article_title')
            elif sort_by == 'title-down':
                article_list = article_list.order_by('-article_title')
            elif sort_by == 'author-up':
                article_list = article_list.order_by('article_author__author_name') 
            elif sort_by == 'author-down':
                article_list = article_list.order_by('-article_author__author_name') 
            elif sort_by == 'date-modified-up':
                article_list = article_list.order_by('modified_at')
            elif sort_by == 'date-modified-down':
                article_list = article_list.order_by('-modified_at')
                
            # Pagination
            # paginator = Paginator(article_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # article_list = paginator.get_page(page_number)
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Articles',
                'session_admin': admin,
                'page_obj': article_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
                
            notes = f'Accessed Articles List'
            record_log(user_id, 5, 11, 0, notes)
            
            return render(request, 'aa2000_admin/articles/articles.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')


def add_article(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                    'nav_title': 'Add New Article',
                    'session_admin': admin,
                    'activities': get_recent_activities()
                    }
            
            notes = f'Accessed Add Article Page'
            record_log(user_id, 5, 11, 0, notes)
            
            return render(request, 'aa2000_admin/articles/add-article.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    
# @require_http_methods(['POST'])
def processadd_article(request):
    try:
        article_data = request.POST
        cover = request.FILES.get('cover')
        author_img = request.FILES.get('author_img')
        
        
        if Article.objects.filter(article_slug=article_data.get('slug')).exists():
            return JsonResponse({
                'status': 'error',
                'error': 'Duplicate Slug',
                'message': 'Article slug already exists.',
            })
        
        article = Article.objects.create(
            article_title=article_data.get('title'),
            article_slug=article_data.get('slug'),
            article_cover=cover,
            keywords=article_data.get('keywords')
        )
        
        ArticleContent.objects.create(
            article=article,
            content=article_data.get('content'),
        )
        
        Author.objects.create(
            article=article,
            author_name=article_data.get('author'),
            author_image=author_img,
            author_description=article_data.get('author_description'),
        )
        
        article_id = article.id
        user_id = request.session.get('user_id')
        notes = f'Added New Article {article.article_title}'
        record_log(user_id, 5, 1, article_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Article added successfully.',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to add article.',
            })
        
def view_article(request, slug):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:

                articleData = Article.objects.select_related(
                    'article_author',  # Prefetch related authors
                    'article_content'  # Prefetch related content
                ).get(article_slug=slug)

                # Access the related authors
                author = articleData.article_author
                content = articleData.article_content  


                
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'View Article',
                'article': articleData,
                'author': author, 
                'content': content,
                'session_admin': admin,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Article Details ({articleData.article_title})'
            article_id = articleData.id
            record_log(user_id, 5, 2, article_id, notes)
            
            return render(request, 'aa2000_admin/articles/view-article.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    


def edit_article(request, slug):
    try:
        # Fetch the article using the slug
        articleData = Article.objects.get(article_slug=slug)
        article_data = request.POST
        cover = request.FILES.get('cover')
        author_img = request.FILES.get('author_img')
        
        # Update the article fields
        articleData.article_title = article_data.get('title')
        articleData.article_slug = article_data.get('slug')  # Correct field name
        articleData.keywords = article_data.get('keywords')
        if cover:
            articleData.article_cover = cover
        articleData.save()  # Save the article changes

        # Update the content data
        contentData = articleData.article_content  # Correctly access the content
        contentData.content = article_data.get('content')
        contentData.save()  # Save the content changes
        
        
        # Update the associated author data
        authorData = articleData.article_author  # Correctly access the author
        authorData.author_name = article_data.get('author')  # Correct field name
        if author_img:
            authorData.author_image = author_img  # Correct field name
        authorData.author_description = article_data.get('author_description')
        authorData.save()  # Save the author changes

        article_id = articleData.id
        user_id = request.session.get('user_id')
        notes = f'Updated Article ({articleData.article_title})'
        record_log(user_id, 5, 3, article_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Article updated successfully.',
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to update article.',
        })

        
def delete_article(request, slug):
    try: 
        article = Article.objects.get(article_slug=slug)
        
        # Use get() instead of filter() to get a single Author object
        author = Author.objects.get(article=article)
        content = ArticleContent.objects.get(article=article)
        
        user_id = request.session.get('user_id') 
        article_id = article.id
        notes = f'Deleted Article {article.article_title}'
        record_log(user_id, 3, 4, article_id, notes)
        
        if author.author_image:
            delete_file(author.author_image.path)
        
        # Delete the related objects and then the article
        author.delete()
        content.delete()
        article.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Article deleted successfully.',
        })
        
    except Author.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Author not found for the article.',
        })
    except ArticleContent.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Article content not found for the article.',
        })
    except Article.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Article not found.',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'message': 'Failed to delete article.',
        })


def delete_file(file_path):
    """Helper function to delete a file from the filesystem."""
    if os.path.isfile(file_path):
        os.remove(file_path)
