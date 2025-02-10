from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         image = request.FILES['file']
#         print("Received image:", image)  # Debugging line to confirm file receipt

#         # Define the upload path and ensure the 'uploads' folder exists
#         upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
#         os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        
#         # Save the uploaded image
#         with open(upload_path, 'wb+') as destination:
#             for chunk in image.chunks():
#                 destination.write(chunk)
        
#         # Construct the image URL
#         image_url = f"{settings.MEDIA_URL}uploads/{image.name}"
#         full_url = request.build_absolute_uri(image_url)
#         print("Image saved at:", full_url)  # Debugging line to confirm save path
        
#         # Return the response
#         return JsonResponse({"location": full_url})

#     print("File upload failed: No file found in request.")  # Debugging line for missing file
#     return JsonResponse({'error': 'File upload failed'}, status=400)




@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            print("❌ No file found in request.")
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        image = request.FILES['file']
        print("✅ Received image:", image.name)  # Debugging line

        # Ensure upload directory exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file
        file_path = os.path.join(upload_dir, image.name)
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Generate absolute URL
        relative_url = f"{settings.MEDIA_URL}uploads/{image.name}"
        full_url = request.build_absolute_uri(relative_url)

        print("✅ Image saved at:", full_url)  # Debugging line
        return JsonResponse({"location": full_url})  # Correct JSON format

    print("❌ Request method not POST")
    return JsonResponse({'error': 'Invalid request'}, status=400)