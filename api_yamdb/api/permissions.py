from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperuser(BasePermission):
    """Admin or superuser access only."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin_or_superuser
        )


class IsAdminOrModeratirOrAuthor(BasePermission):
    """Access method is SAFE_METHODS or user is authenticated.
    admin or superuser access all requests."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """The request method is SAFE_METHODS or admin access only."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )
