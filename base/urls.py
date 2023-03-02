from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('add_material/', views.add_material, name='add_material'),
    path('materials/<int:pk>/update/', views.update_material, name='update_material'),
    path('materials/pending/', views.pending_materials, name='pending_materials'),
    path('materials/<int:pk>/delete/', views.delete_material, name='delete_material'),
    path('materials/<int:pk>/download/', views.download_file, name='download_file'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('google-login/', views.google_login, name='google-login'),
    path('google-authenticate/', views.google_authenticate, name='google-authenticate'),

]
