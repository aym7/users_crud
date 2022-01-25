from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admin creators of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """ Read permissions are allowed to any request,
        Write permissions are only allowed to the creator of the customer.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
