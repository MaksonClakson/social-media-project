from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.contrib.auth import get_user_model

from users.models import User
from api.models import Page


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and (request.user.is_staff or request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.owner == request.user) or request.user.is_staff


class IsPostOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Is Post Owner Or Admin Or Read Only Permission
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and (request.user.is_staff or request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.page.owner == request.user) or request.user.is_staff


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.user


class IsPageOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        page = get_object_or_404(Page, pk=view.kwargs.get('pk'))
        if request.user and request.user.is_authenticated and request.user == page.owner:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPageRequestsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        page = get_object_or_404(Page, pk=view.kwargs.get('page_pk'))
        if request.user and request.user.is_authenticated and request.user == page.owner:
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == str(User.Roles.ADMIN))


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == str(User.Roles.USER))


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == str(User.Roles.MODERATOR)))


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)


class IsSelfUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print("IsSelfUser1")
        user = get_object_or_404(get_user_model(), pk=view.kwargs.get('pk'))
        if request.user and request.user.is_authenticated and request.user == user:
            return True
        return False
