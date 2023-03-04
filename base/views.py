import os
import smtplib

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse

from Bstore import settings
from .models import Course, Topic, Material
from .forms import MaterialForm, MaterialUpdateForm, UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow


# Create your views here.
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


def download_file(request, pk):
    my_object = get_object_or_404(Material, pk=pk)
    file_path = my_object.file.path
    file_name = os.path.basename(file_path)
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    return response


def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def categories(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)


def blog(request):
    return render(request, 'blog.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        body = request.POST.get('message', '')

        send_email(name, email, number, body)

        return render(request, 'success.html')

    return render(request, 'contact.html')


def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")

    topics = Topic.objects.filter(course=course)
    materials = Material.objects.filter(course=course)
    context = {'course': course, 'topics': topics, 'materials': materials}
    return render(request, 'course_detail.html', context)


@login_required(login_url='login')
def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['file']
            course = form.cleaned_data['course']
            topic = form.cleaned_data['topic']
            description = form.cleaned_data['description']
            new_topic_name = form.cleaned_data['new_topic_name']
            new_course_name = form.cleaned_data['new_course_name']

            # Create new topic if new_topic_name is provided
            if new_topic_name:
                topic = Topic(name=new_topic_name, course=course)
                topic.save()

            # Create new course if new_course_name is provided
            if new_course_name:
                existing_course = Course.objects.filter(name=new_course_name).exists()
                if existing_course:
                    messages.error(request, f"This course, {new_course_name} exists already select from the dropdown list")
                    return redirect('home')
                else:
                    course = Course(name=new_course_name)
                    course.save()

            # Check for existing materials with the same name and course/topic combination
            existing_material = Material.objects.filter(name=name, topic=topic, course=course).exists()
            if existing_material:
                messages.error(request, f"The material, {existing_material} or course exists already")
                return redirect('home')

            # Save the user

            # Save the new material
            material = Material(name=name, file=file, course=course, topic=topic, description=description,
                                uploaded_by=request.user)
            material.save()
            messages.success(request, "Thank you for your contribution, the material is now under review")
            return redirect('home')
    else:
        form = MaterialForm()

    context = {'form': form}
    return render(request, 'add_material.html', context)


@user_passes_test(lambda u: u.is_staff)
@staff_member_required
def update_material(request, pk):
    is_admin = request.user.is_staff
    material = get_object_or_404(Material, id=pk)
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


@staff_member_required
def pending_materials(request):
    materials = Material.objects.filter(reviewed=False)
    return render(request, 'pending_materials.html', {'materials': materials})


@staff_member_required
def delete_material(request, pk):
    material = get_object_or_404(Material, id=pk)
    material.delete()
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect('register')
        user = User.objects.create_user(email, email, password1)
        user.save()
        login(request, user)
        messages.success(request, "You are now registered and logged in")
        return redirect('home')
    else:
        return render(request, 'register.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def google_login(request):
    flow = Flow.from_client_config(
        settings.GOOGLE_CLIENT_SECRETS,
        scopes=['openid', 'email', 'profile'],
        redirect_uri=request.build_absolute_uri(reverse('google-authenticate'))
    )
    authorization_url, state = flow.authorization_url(prompt='select_account')
    request.session['oauth_state'] = state
    return redirect(authorization_url)


def google_authenticate(request):
    state = request.session.pop('oauth_state', '')
    flow = Flow.from_client_config(
        settings.GOOGLE_CLIENT_SECRETS,
        scopes=['openid', 'email', 'profile'],
        state=state,
        redirect_uri=request.build_absolute_uri(reverse('google-authenticate'))
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    id_token_info = id_token.verify_oauth2_token(
        flow.credentials.id_token, Request(), settings.GOOGLE_CLIENT_ID)
    email = id_token_info['email']
    user = authenticate(request, email=email)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return HttpResponseBadRequest('Invalid user')


def send_email(name, email, phone, message):
    OWN_EMAIL = os.environ.get('EMAIL_ADD')
    OWN_PASSWORD = os.environ.get('EMAIL_PASS')
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        # connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail('Bstore', OWN_EMAIL, email_message)


def api_doc(request):
    return render(request, 'api_doc.html')