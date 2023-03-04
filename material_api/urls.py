from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='course-list'),
    path('courses/<uuid:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('topics/', views.TopicList.as_view(), name='topic-list'),
    path('topics/<uuid:pk>/', views.TopicDetail.as_view(), name='topic-detail'),
    path('materials/', views.MaterialList.as_view(), name='material-list'),
    path('materials/<uuid:pk>/', views.MaterialDetail.as_view(), name='material-detail'),
    # obtain JWT token pair
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # refresh JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
