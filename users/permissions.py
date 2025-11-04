from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperuserOrReadOnly(BasePermission):
    """
    Lecture pour tout utilisateur authentifié (géré par IsAuthenticated au niveau de la vue).
    Écriture (POST, PUT, PATCH, DELETE) réservée aux superusers.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)