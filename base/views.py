import os

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Course, Topic, Material
from .forms import MaterialForm, MaterialUpdateForm, UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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
    return render(request, 'contact.html')


def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")

    topics = Topic.objects.filter(course=course)
    materials = Material.objects.filter(course=course)
    context = {'course': course, 'topics': topics, 'materials': materials}
    return render(request, 'course_detail.html', context)


def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['file']
            course = form.cleaned_data['course']
            topic = form.cleaned_data['topic']
            new_topic_name = form.cleaned_data['new_topic_name']
            new_course_name = form.cleaned_data['new_course_name']

            # Create new topic if new_topic_name is provided
            if new_topic_name:
                topic = Topic(name=new_topic_name, course=course)
                topic.save()

            # Create new course if new_course_name is provided
            if new_course_name:
                course = Course(name=new_course_name)
                course.save()

            # Check for existing materials with the same name and course/topic combination
            existing_material = Material.objects.filter(name=name, course=course, topic=topic).exists()
            if existing_material:
                return redirect('home')

            # Save the new material
            material = Material(name=name, file=file, course=course, topic=topic)
            material.save()

            return redirect('home')
    else:
        form = MaterialForm()

    context = {'form': form}
    return render(request, 'add_material.html', context)


def update_material(request, pk):
    material = get_object_or_404(Material, id=pk)
    form = MaterialUpdateForm(request.POST or None, request.FILES or None, instance=material)

    if form.is_valid():
        material = form.save(commit=False)
        material.topic = form.cleaned_data['topic']
        material.course = form.cleaned_data['course']
        material.save()
        return redirect('course_detail', course_id=material.course.pk)

    context = {
        'form': form,
        'material': material,
    }

    return render(request, 'update_material.html', context)


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
        messages.success(request, "You are now registered and can log in")
        return redirect('home')
    else:
        return render(request, 'register.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
