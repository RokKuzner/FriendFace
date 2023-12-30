from django.http import HttpResponse
from FriendFace.settings import BASE_DIR
import os

STATIC_URL = os.path.join(BASE_DIR, "static")
JAVASCRIPT_URL = os.path.join(STATIC_URL, "javascript")
CSS_URL = os.path.join(STATIC_URL, "css")
ICONS_URL = os.path.join(STATIC_URL, "icons")

MEDIA_URL = os.path.join(BASE_DIR, "media")
AVATARS_URL = os.path.join(MEDIA_URL, "avatars")


# Views
def profileimg(request):
    user_id = request.GET.get('user', None)

    image_path = os.path.join(AVATARS_URL, f"{user_id}.jpg")
    image_name = f"{user_id}.jpg"

    if os.path.exists(image_path) == False:
        response = HttpResponse()
        response['Content-Type'] = 'image/jpeg'
        return response


    # Open the image file in binary mode
    with open(image_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type="image/jpeg")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={image_name}"

        return response
    
def js(request):
    file = request.GET.get('file', None)

    file_path = os.path.join(JAVASCRIPT_URL, f"{file}.js")
    file_name = f"{file}.js"

    if os.path.exists(file_path) == False:
        response = HttpResponse()
        response['Content-Type'] = 'text/javascript'
        return response

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type="text/javascript")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={file_name}"

        return response
    
def css(request):
    file = request.GET.get('file', None)

    file_path = os.path.join(CSS_URL, f"{file}.css")
    file_name = f"{file}.css"

    if os.path.exists(file_path) == False:
        response = HttpResponse()
        response['Content-Type'] = 'text/css'
        return response

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type="text/css")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={file_name}"

        return response

def logo(request):
    file_path = os.path.join(STATIC_URL, "friendface_logo.png")
    file_name = "friendface_logo.png"

    with open(file_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type=f"image/png")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={file_name}"

        return response

def favicon(request):
    file_path = os.path.join(STATIC_URL, "favicon.ico")
    file_name = "favicon.ico"

    with open(file_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type=f"image/vnd.microsoft.icon")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={file_name}"

        return response

def icons(request):
    file = request.GET.get('file', None)

    file_path = os.path.join(ICONS_URL, file)
    file_name = file

    if os.path.exists(file_path) == False:
        response = HttpResponse()
        response['Content-Type'] = 'image/png'
        return response
    
    not_important, file_extension = os.path.splitext(file_path)

    if file_extension == ".jpg":
        file_extension = ".jpeg"

    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Create an HttpResponse object
        response = HttpResponse(f.read(), content_type=f"image/{file_extension[1:]}")

        # Set the Content-Disposition header
        response["Content-Disposition"] = f"inline; filename={file_name}"

        return response