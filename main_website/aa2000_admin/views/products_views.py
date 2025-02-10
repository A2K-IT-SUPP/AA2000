from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.contrib import messages
import json, os
from django.conf import settings
from django.views.decorators.http import require_http_methods
# import logging, os
# from django.utils.text import slugify
# from datetime import datetime


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

from .logs_views import record_log, get_recent_activities






# categories
def get_categories(request):
    system_id = request.GET.get('system')  
    categories = ProductCategory.objects.filter(system_id=system_id)
    brands = Brand.objects.filter(system_id=system_id)
    if categories.exists():
        return JsonResponse({
            'success': True,
            'categories': [{'id': category.id, 'name': category.category_name} for category in categories],
            'brands': [{'id': brand.id, 'name': brand.brand_name} for brand in brands]
            
        })
    else:
        return JsonResponse({'success': False, 'message': 'No categories found.'})


#products -----------------------------------------------------------------------------------------------------------
def products(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            sort_by = request.GET.get('sort_by', 'id-down')  # Default sort option
            filter_search_by = request.GET.get('filter_search_by', 'id')
            search_query = request.GET.get('search', '').strip()
            
            # product_list = Product.objects.select_related('system', 'category', 'brand').prefetch_related('product_photos')

            product_list = Product.objects.select_related(
                'system', 
                'category', 
                'brand'
            ).prefetch_related(
                Prefetch(
                    'product_photos',
                    queryset=ProductPhoto.objects.order_by('id')[:1],
                    to_attr='first_photo'
                )
            )
            
            if search_query:
                if filter_search_by == 'id':
                    product_list = product_list.filter(id__icontains=search_query)
                elif filter_search_by == 'name':
                    product_list = product_list.filter(product_name__icontains=search_query)
                elif filter_search_by == 'system':
                    product_list = product_list.filter(system__system_name__icontains=search_query)
                elif filter_search_by == 'category':
                    product_list = product_list.filter(product_details__category__category_name__icontains=search_query)
                elif filter_search_by == 'date-modified':
                    product_list = product_list.filter(modified_at__icontains=search_query)

            if sort_by == 'id-up':
                product_list = product_list.order_by('id')
            elif sort_by == 'id-down':
                product_list = product_list.order_by('-id')
            elif sort_by == 'name-up':
                product_list = product_list.order_by('product_name')  # Sort by first and last name
            elif sort_by == 'name-down':
                product_list = product_list.order_by('-product_name')  # Sort by first and last name descending
            elif sort_by == 'date-modified-up':
                product_list = product_list.order_by('modified_at')
            elif sort_by == 'date-modified-down':
                product_list.order_by('-modified_at')
                
            # Pagination
            # paginator = Paginator(product_list, 10)  # Show 10 admins per page
            # page_number = request.GET.get('page')
            # product_list = paginator.get_page(page_number)
            
            current_time = timezone.now()
            page_details = {
                'current_time': current_time,
                'nav_title': 'Products',
                'session_admin': admin,
                'page_obj': product_list,
                'sort_by': sort_by,
                'filter_search_by': filter_search_by,
                'search_query': search_query,
                'activities': get_recent_activities()
            }
            
            notes = f'Accessed Products List'
            record_log(user_id, 4, 11, 0, notes)
            
            return render(request, 'aa2000_admin/products/products.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    


def add_product(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
            current_time = timezone.now()
            
            systems = System.objects.all()
            brands = Brand.objects.all()
            
            
            page_details = {'current_time': current_time,
                    'nav_title': 'Add New Product',
                    'session_admin': admin,
                    'systems': systems,
                    'brands': brands,
                    'activities': get_recent_activities()
                    }
            
            notes = f'Accessed Add Product Page'
            record_log(user_id, 4, 11, 0, notes)
            
            return render(request, 'aa2000_admin/products/add-product.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')
    

@require_http_methods(['POST'])
def add_product_overview(request):

    try:
        
        data = {
            'name': request.POST.get('productName'),
            'slug': request.POST.get('productSlug'),
            'system_id': request.POST.get('productSystem'),
            'category_id': request.POST.get('productCategory'),
            'brand_id': request.POST.get('productBrand'),
            'short_description': request.POST.get('productShortDescription')
        }
        
        if Product.objects.filter(product_slug=data['slug']).exists():
            print('existing slug found')
            return JsonResponse({
                'status': 'error',
                'error': 'product slug',
                'message': 'Product with this slug already exists.',
                'fields': {
                    'productName': data['name'],
                    'productSlug': data['slug'],
                    'productSystem': data['system_id'],
                    'productCategory': data['category_id'],
                    'productBrand': data['brand_id'],
                    'productShortDescription': data['short_description']
                }
            })
        
        product = Product.objects.create(
            product_name=data['name'],
            product_slug=data['slug'],
            system_id=data['system_id'],
            category_id=data['category_id'],
            brand_id=data['brand_id'],
            short_description=data['short_description']
        )
        
        user_id = request.session.get('user_id')
        product_id = product.id
        notes = f'Added New Product Overview ({product.product_name}) '
        record_log(user_id, 4, 1, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product Created Successfully',
            'product': {
                'id': product.id,
                'name': product.product_name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        


@require_http_methods(['POST'])
def add_product_photos(request):
    
    try:
        # Debug print
        print("Received data:", request.POST)
        print("Received files:", request.FILES)
        
        # Validate productId
        product_id = request.POST.get('productId')
        if not product_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Product ID is required'
            }, status=400)
            
        # Get product or return 404
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Product with ID {product_id} not found'
            }, status=404)
        
        # Handle each photo upload
        photos_added = 0
        for i in range(1, 4):
            photo_key = f'productImg{i}Upload'
            if photo_key in request.FILES:
                ProductPhoto.objects.create(
                    product=product,
                    product_image=request.FILES[photo_key]
                )
                photos_added += 1
                
        user_id = request.session.get('user_id')
        product_id = product.id
        notes = f'Added New Product Photos ({product.product_name}) '
        record_log(user_id, 4, 1, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Successfully added {photos_added} product photos',
            'photos_added': photos_added,
            'product': {
                'id': product_id,
            }
        })
        
    except Exception as e:
        print(f"Error in add_product_photos: {str(e)}")  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
        
@require_http_methods(['POST'])
def add_product_description(request):
    try:
        productId = request.POST.get('productId')
        # product = get_object_or_404(id=productId)
        
        for i in range(1,3):
            productDescription_key = f'productDescription_{i}'
            productDescImgUpload_key = f'productDescImg{i}Upload'
            
            if request.FILES.get(productDescImgUpload_key):
                photo_key = request.FILES.get(productDescImgUpload_key)
            
                productDescription = ProductDescription.objects.create(
                    product_id=productId,
                    product_description=request.POST.get(productDescription_key),
                    product_image=photo_key
                )
                productDescription.save()
                
        user_id = request.session.get('user_id')
        product = Product.objects.get(id=productId)
        notes = f'Added New Product Description ({product.product_name}) '
        record_log(user_id, 4, 1, productId, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product description added successfully',
            'product': {
                'id': productId
                }
        })
            
            
    except Exception as e:
        print(f"Error in add_product_description: {str(e)}")  # Debug print
        return JsonResponse({
            'status': 'error',
            'message': str(e)
            }, status=400)

@require_http_methods(['POST'])
def add_product_key_features(request):
    
    try:
        product = get_object_or_404(Product, id=request.POST.get('productId'))
        
        for i in range(1,3):
            feature_text = request.POST.get(f'keyFeature_{i}')
            if feature_text:
                feature = KeyFeature.objects.create(
                    product=product,
                    key_feature=feature_text
                )
                
                image_key = f'keyFeatureImg{i}Upload'
                if image_key in request.FILES:
                    feature.key_feature_image=request.FILES[image_key]
                    feature.save()
                    
        user_id = request.session.get('user_id')
        product_id = product.id
        notes = f'Added New Product Key Features ({product.product_name}) '
        record_log(user_id, 4, 1, product_id, notes)
                    
        return JsonResponse({
            'status': 'success',
            'message': 'Key Features Added Successfully',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
            }, status=400)
    
    
    


@require_http_methods(['POST'])
def add_product_technical_specs(request):
    try:
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('productId'))
        
        for category in data.get('categories', []):
            tech_spec = TechSpec.objects.create(
                product=product,
                tech_spec=category.get('category_name', '')
                )
            
            for spec in category.get('specifications', []):
                TechSpecDetails.objects.create(
                    tech_spec=tech_spec,
                    tech_spec_name=spec.get('name'),
                    tech_spec_value=spec.get('value'),
                )
                
        user_id = request.session.get('user_id')
        product_id = product.id
        notes = f'Added New Product Technical Specifications ({product.product_name}) '
        record_log(user_id, 4, 1, product_id, notes)
        
        return JsonResponse({
            'status': "success",
            "message": "Technical Specs Saved Successfully"
        })
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    

def view_product(request, slug):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)  
            admin = Admin.objects.get(user=user)  
        
            try:

                
                productData = Product.objects.select_related(
                    'brand',
                    'system',
                    'category'
                ). prefetch_related(
                    'product_photos',
                    'product_descriptions',
                    'key_features',
                    Prefetch(
                        'product_techSpec',
                        queryset=TechSpec.objects.prefetch_related('tech_spec_details')
                    )
                ).get(product_slug=slug)
                
                productPhotos = productData.product_photos.all()
                productDescriptions = productData.product_descriptions.all()
                productKeyFeatures = productData.key_features.all()
                productTechSpecs = productData.product_techSpec.all()
                
                systems = System.objects.all()
                category = ProductCategory.objects.filter(system_id=productData.system_id)
                brands = Brand.objects.filter(system_id=productData.system_id)
                
            except Admin.DoesNotExist:
                raise Http404("Profile Does Not Exists")
            
            current_time = timezone.now()
            page_details = {'current_time': current_time,
                            'nav_title': 'View Product',
                            'systems': systems,
                            'categories': category,
                            'productData': productData,
                            'brands': brands, 
                            'productPhotos': productPhotos,
                            'productDescriptions': productDescriptions,
                            'productKeyFeatures': productKeyFeatures,
                            'productTechSpecs': productTechSpecs,
                            'session_admin': admin,
                            'activities': get_recent_activities()
                            }
            
            notes = f'Accessed Product Details ({productData.product_name})'
            product_id = productData.id
            record_log(user_id, 4, 2, product_id, notes)
            
            return render(request, 'aa2000_admin/products/view-product.html', page_details)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'aa2000_admin/index.html')
        except Admin.DoesNotExist:
            messages.error(request, 'Admin details not found.')
            return render(request, 'aa2000_admin/index.html')
    else:
        messages.warning(request, 'You need to be logged in to access this page.')
        return render(request, 'aa2000_admin/index.html')


@require_http_methods(['POST'])
def edit_product_overview(request, slug):

    try:
        
        product = Product.objects.get(product_slug=slug)
        
        data = {
            'product_name': request.POST.get('productName'),
            'product_slug': request.POST.get('productSlug'),
            'system_id': request.POST.get('productSystem'),
            'category_id': request.POST.get('productCategory'),
            'brand_id': request.POST.get('productBrand'),
            'short_description': request.POST.get('productShortDescription')
        }
        
        if product:
            product.product_name = data['product_name']
            product.product_slug = data['product_slug']
            product.system_id = data['system_id']
            product.category_id = data['category_id']
            product.brand_id = data['brand_id']
            product.short_description = data['short_description']
            product.save()
            
            product_id = product.id
            user_id = request.session.get('user_id')
            notes = f'Updated Product Overview ({product.product_name})'
            record_log(user_id, 4, 3, product_id, notes)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Product Overview Updated Successfully',
                'slug': product.product_slug
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            }, status=400)


@require_http_methods(['POST'])
def edit_product_photos(request, slug):
    product = Product.objects.get(product_slug=slug)
    try:
            
        for i in range(1,4):
            photo_file = request.FILES.get(f'productImg{i}Upload')
            photo_id = request.POST.get(f'productImg{i}Id')

            if photo_file:
                print(photo_file)
                print(photo_id)
                productPhoto = ProductPhoto.objects.get(id=photo_id, product_id=product.id)
                productPhoto.product_image = photo_file
                productPhoto.save()
                
        product_id = product.id
        user_id = request.session.get('user_id')
        notes = f'Updated Product Photos ({product.product_name})'
        record_log(user_id, 4, 3, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product Photos Updated Successfully',
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found',
        }, status=404)

    except ProductPhoto.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Photo ID not found for this product',
        }, status=404)

    except Exception as e :
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            }, status=400)


@require_http_methods(['POST'])
def edit_product_description(request, slug):
    try:
        # Get the product based on the slug
        product = Product.objects.get(product_slug=slug)

        # Loop through the submitted descriptions
        for i in range(1, 4):  # Assuming you have a maximum of 3 descriptions
            description_id = request.POST.get(f'descriptionId_{i}')
            product_description = request.POST.get(f'productDescription_{i}')
            product_desc_img = request.FILES.get(f'productDescImg{i}Upload')

            # Get the corresponding ProductDescription instance
            if description_id:
                product_description_instance = ProductDescription.objects.get(id=description_id, product=product)

                # Update the fields
                product_description_instance.product_description = product_description
                if product_desc_img:  # Only update if a new image is provided
                    product_description_instance.product_image = product_desc_img

                # Save the updated instance
                product_description_instance.save()
                
        product_id = product.id
        user_id = request.session.get('user_id')
        notes = f'Updated Product Description ({product.product_name})'
        record_log(user_id, 4, 3, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product descriptions updated successfully.',
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found.',
        }, status=404)
    
    except ProductDescription.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product description not found.',
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=400)    

@require_http_methods(['POST'])
def edit_product_key_features(request, slug):
    try:
        # Get the product based on the slug
        product = Product.objects.get(product_slug=slug)

        # Loop through the submitted descriptions
        for i in range(1, 4):  # Assuming you have a maximum of 3 descriptions
            keyFeature_id = request.POST.get(f'keyFeatureId_{i}')
            key_feature = request.POST.get(f'keyFeature_{i}')
            key_feature_img = request.FILES.get(f'keyFeatureImg{i}Upload')

            # Get the corresponding ProductDescription instance
            if keyFeature_id:
                key_feature_instance = KeyFeature.objects.get(id=keyFeature_id, product=product)

                # Update the fields
                key_feature_instance.key_feature = key_feature
                if key_feature_img:  # Only update if a new image is provided
                    key_feature_instance.key_feature_image = key_feature_img

                # Save the updated instance
                key_feature_instance.save()
                
        product_id = product.id
        user_id = request.session.get('user_id')
        notes = f'Updated Product Key Features ({product.product_name})'
        record_log(user_id, 4, 3, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product key features updated successfully.',
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found.',
        }, status=404)
    
    except KeyFeature.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Key Features not found.',
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=400)    

# @require_http_methods(['POST'])
def edit_product_technical_specs(request, slug):
    try:
        
        product = Product.objects.get(product_slug=slug)
        data = json.loads(request.body)

        existing_specs = {spec.id: spec for spec in TechSpec.objects.filter(product=product)}
        existing_details = {detail.id: detail for detail in TechSpecDetails.objects.filter(tech_spec__product=product)}

        incoming_spec_ids = set()
        incoming_detail_ids = set()

        for category in data.get('categories', []):
            category_id = category.get('categoryId')
            incoming_spec_ids.add(category_id)

            tech_spec = existing_specs.get(category_id)
            if tech_spec:
                
                tech_spec.tech_spec = category.get('categoryName')
                tech_spec.save()
            else:
                
                tech_spec = TechSpec.objects.create(
                    product=product,
                    tech_spec=category.get('categoryName')
                )

            for spec in category.get('specifications', []):
                spec_id = spec.get('specCategId')
                incoming_detail_ids.add(spec_id)

                tech_spec_detail = existing_details.get(spec_id)
                if tech_spec_detail:
                    
                    tech_spec_detail.tech_spec_name = spec.get('name')
                    tech_spec_detail.tech_spec_value = spec.get('value')
                    tech_spec_detail.save()
                else:
                    
                    TechSpecDetails.objects.create(
                        tech_spec=tech_spec,
                        tech_spec_name=spec.get('name'),
                        tech_spec_value=spec.get('value')
                    )

        for spec_id, spec in existing_specs.items():
            if spec_id not in incoming_spec_ids:
                spec.delete()

        for detail_id, detail in existing_details.items():
            if detail_id not in incoming_detail_ids:
                detail.delete()

        product_id = product.id
        user_id = request.session.get('user_id')
        notes = f'Updated Product Technical Specifications ({product.product_name})'
        record_log(user_id, 4, 3, product_id, notes)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product technical specs updated successfully.',
            'slug':  product.product_slug

        })

    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found.',
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=400)
        
        
        
        
def delete_product(request, slug):
    try:
        
        product = Product.objects.get(product_slug=slug)
        
    
        techspecdetails = TechSpecDetails.objects.filter(tech_spec__product=product)
        techspecs = TechSpec.objects.filter(product=product)
        keyfeatures = KeyFeature.objects.filter(product=product)
        descriptions = ProductDescription.objects.filter(product=product)
        photos = ProductPhoto.objects.filter(product=product)

        for photo in photos:
            if photo.product_image:
                delete_file(photo.product_image.path)
        
        
        for description in descriptions:
            if description.product_image:
                delete_file(description.product_image.path)
                
        for keyfeature in keyfeatures:
            if keyfeature.key_feature_image:
                delete_file(keyfeature.key_feature_image.path)
                
        
        
        techspecdetails.delete()
        techspecs.delete()
        keyfeatures.delete()
        descriptions.delete()
        photos.delete()
        
        product_id = product.id
        user_id = request.session.get('user_id')
        notes = f'Deleted Product Technical Specifications ({product.product_name})'
        record_log(user_id, 4, 4, product_id, notes)
        
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product deleted successfully.'
            }, status=200)
        
    
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred: {}'.format(str(e))
        }, status=500)

def delete_file(file_path):
    """Helper function to delete a file from the filesystem."""
    if os.path.isfile(file_path):
        os.remove(file_path)