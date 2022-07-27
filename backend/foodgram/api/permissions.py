from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (not request.user.is_anonymous
                    and request.user.is_admin))


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (not request.user.is_anonymous
                and request.user.is_admin)


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author)
