from rest_framework import permissions

class IsNotAuthenticated(permissions.BasePermission):
    """
    Global permission to check user authentication status.
    You can block access to some urls for authenticated
    users.
    """

    def has_permission(self, request, view):
        if request in permissions.SAFE_METHODS:
            return True

        return bool(not request.user.is_authenticated)


class IsUserProfileOwner(permissions.BasePermission):
    """
    Check if authenticated user is owner of the profile
    """

    def has_object_permission(self, request, view, obj):
        x = bool(request.user.is_authenticated)
        y = obj.user == request.user or request.user.is_staff
        return x and y