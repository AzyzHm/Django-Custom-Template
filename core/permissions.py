from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level permission allowing access only to the resource's owner."""

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner_id == request.user.id
