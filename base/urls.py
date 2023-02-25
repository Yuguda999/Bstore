from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('course/', views.course, name='course'),
    path('books/', views.books, name='books'),
    path('upload/', views.upload_file, name='upload'),
    path('view/<str:pk>/', views.download_file, name='upload'),
    path('books/<int:pk>/update/', views.update_book, name='book_update'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]
