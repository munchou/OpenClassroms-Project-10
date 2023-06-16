from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return request.user.is_author


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_contributor
