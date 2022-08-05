from rest_framework.permissions import BasePermission
from rest_framework import permissions

class CustomPermission(permissions.BasePermission):


    PERMISSION_CHECKING_URLS=['PATCH']
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            return False