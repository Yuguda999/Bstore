# from rest_framework.permissions import BasePermission, SAFE_METHODS
#
#
# class IsAdminOrReadOnly(BasePermission):
#     """
#     The request is authenticated as an admin, or is a read-only request.
#     """
#
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#
#         return request.user.is_staff
