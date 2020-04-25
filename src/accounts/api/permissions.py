from rest_framework import permissions

class AnonPermissionOnly(permissions.BasePermission):
    message = 'You are already authenticated. Please log out to try again.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated



class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user



class IsUserPresent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
