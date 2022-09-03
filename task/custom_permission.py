import rest_framework 

class IsOwner(rest_framework.permissions.BasePermission):
    """
    Allows access only to owner users.
    """

    def has_permission(self, request, view):
        

        return bool(request.user and request.user.is_authenticated)
