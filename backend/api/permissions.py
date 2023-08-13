from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermission(BasePermission):
    """Permission для автора рецепта."""
    def has_object_permission(self, request, view, obj) -> bool:
        return request.method in SAFE_METHODS or obj.author == request.user
