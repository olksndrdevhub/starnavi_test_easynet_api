from rest_framework.permissions import BasePermission, SAFE_METHODS



SAFE_METHODS = ['POST']

class IsAdminOrCreateOnly(BasePermission):
    """
    Perrmisson to allow create new account but not allow 
    non-admin users get the users list
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser):
            return True
        return False