import os
from io import BytesIO

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
from django.http import Http404

from Bstore import settings
from .models import Course, Topic, Material
from .forms import MaterialForm, MaterialUpdateForm
from base.email import send_email, email_new_user

# Load environment variables from .env file
load_dotenv()

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize Google Drive API credentials from the credentials file
credentials = service_account.Credentials.from_service_account_file(
    settings.GOOGLE_DRIVE_CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/drive']
)


# ---------------------- Views ----------------------

# Home view
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        body = request.POST.get('message', '')
        send_email(name, email, number, body)
        messages.success(request, "Message Sent Successfully")
        return redirect('home')

    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'index.html', context)


# About view
def about(request):
    return render(request, 'about.html')


# Categories view
def categories(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)


# Blog view
def blog(request):
    return render(request, 'blog.html')


# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        body = request.POST.get('message', '')
        send_email(name, email, number, body)
        messages.success(request, "Message Sent Successfully")
        return redirect('home')

    return render(request, 'contact.html')


# Course detail view
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")

    topics = Topic.objects.filter(course=course)
    materials = Material.objects.filter(course=course)
    context = {'course': course, 'topics': topics, 'materials': materials}
    return render(request, 'course_detail.html', context)


# Search view
def search(request):
    query = request.GET.get('q')
    print(query)
    results = None
    if query:
        results = Material.objects.filter(
            Q(name__icontains=query) |
            Q(topic__name__icontains=query) |
            Q(course__name__icontains=query)
        )
        print(results)
    context = {
        'query': query,
        'materials': results
    }
    return render(request, 'search.html', context)


# Download file view
@login_required(login_url='login')
def download_file(request, pk):
    try:
        file_instance = Material.objects.get(id=pk)
        drive_service = build('drive', 'v3', credentials=credentials)

        file_metadata = drive_service.files().get(fileId=file_instance.drive_id).execute()
        file_name = file_metadata['name']
        file_mime_type = file_metadata['mimeType']
        file_bytes = drive_service.files().get_media(fileId=file_instance.drive_id).execute()

        # Create an in-memory file-like object
        file_object = BytesIO(file_bytes)

        response = HttpResponse(content_type=file_mime_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        response.write(file_object.getvalue())

        return response
    except Material.DoesNotExist:
        raise Http404("File not found")
    except Exception as e:
        return HttpResponse(f"Error occurred while downloading the file: {e}", status=500)


# Add material view
@login_required(login_url='login')
def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            # ... Code for material creation ...

            try:
                # Save the new material
                material_instance = Material.objects.create(name=name, drive_id=created_file['id'], course=course, topic=topic,
                                                            description=description, uploaded_by=request.user)
                messages.success(request, "Thank you for your contribution, the material is now under review")
                return redirect('home')
            except Exception as e:
                return HttpResponse(f"Error occurred while adding the material: {e}", status=500)

    else:
        form = MaterialForm()

    context = {'form': form}
    return render(request, 'add_material.html', context)


# Course update view
@user_passes_test(lambda u: u.is_staff)
@staff_member_required
def update_material(request, pk):
    try:
        material = Material.objects.get(id=pk)
    except Material.DoesNotExist:
        raise Http404("Material does not exist")

    form = MaterialUpdateForm(request.POST or None, request.FILES or None, instance=material)

    if form.is_valid():
        material = form.save(commit=False)
        material.topic = form.cleaned_data['topic']
        material.course = form.cleaned_data['course']
        material.description = form.cleaned_data['description']
        material.save()
        return redirect('pending_materials')

    context = {
        'form': form,
        'material': material,
    }

    return render(request, 'update_material.html', context)


# Pending materials view
@staff_member_required
def pending_materials(request):
    materials = Material.objects.filter(reviewed=False)
    return render(request, 'pending_materials.html', {'materials': materials})


# Delete material view
@staff_member_required
def delete_material(request, pk):
    try:
        file_instance = Material.objects.get(id=pk)
        drive_service = build('drive', 'v3', credentials=credentials)

        drive_service.files().delete(fileId=file_instance.drive_id).execute()

        material = get_object_or_404(Material, id=pk)
        material.delete()
        # Handle the response or redirect to the appropriate page
        return redirect('home')
    except Material.DoesNotExist:
        raise Http404("Material not found")


# ---------------------- Authentication Views ----------------------

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        return render(request, 'login.html')


# Register view
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('register')

        # send welcome message to new user
        email_new_user(username=username, email=email)

        user = User.objects.create_user(username, email, password1)
        user.save()
        login(request, user)
        messages.success(request, "You are now registered and logged in")
        return redirect('home')
    else:
        return render(request, 'register.html')


# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# ---------------------- Miscellaneous Views ----------------------

# API Documentation view
def api_doc(request):
    return render(request, 'api_doc.html')


# ---------------------- Error Handlers ----------------------

# 404 Page Not Found handler
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# 500 Server Error handler
def server_error(request):
    return render(request, '500.html', status=500)
