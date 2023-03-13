from rest_framework.permissions import BasePermission


class IsSupportUserPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.create and request.create.is_staff_user)
