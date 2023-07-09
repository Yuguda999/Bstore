# from rest_framework import generics
# from rest_framework_simplejwt.authentication import JWTAuthentication
#
# from base.models import Course, Topic, Material
# from .serializers import CourseSerializer, TopicSerializer, MaterialSerializer
# from .permissions import IsAdminOrReadOnly
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAdminUser
#
#
# class CourseList(generics.ListCreateAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# class TopicList(generics.ListCreateAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer
#
#
# class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer
#
#
# class MaterialList(generics.ListCreateAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer
#
#
# class MaterialDetail(generics.RetrieveUpdateDestroyAPIView):
#     authentication_classes = [SessionAuthentication, JWTAuthentication, IsAdminOrReadOnly]
#     permission_classes = [IsAdminUser]
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer
