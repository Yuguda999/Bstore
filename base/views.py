import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, BookFormCleared
from.models import Book

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'upload.html', {'form': form})


def download_file(request, pk):
    my_object = get_object_or_404(Book, pk=pk)
    file_path = my_object.file.path
    file_name = os.path.basename(file_path)
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    return response


def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookFormCleared(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookFormCleared(instance=book)
    return render(request, 'update_book.html', {'form': form, 'pk':pk})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('home')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def categories(request):
    return render(request, 'categories.html')


def blog(request):
    return render(request, 'blog.html')


def contact(request):
    return render(request, 'contact.html')


def course(request):
    return render(request, 'courses.html')


def books(request):
    return render(request, 'books.html')

