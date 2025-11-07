from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSelfOrSuperuserOrReadOnly(BasePermission):
    """
    Lecture: autorisée aux utilisateurs authentifiés (gérée par IsAuthenticated).
    Écriture:
      - superuser: autorisée sur tout le monde
      - utilisateur standard: autorisée uniquement sur son propre objet User
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if getattr(view, "action", None) == "create":
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and (request.user.is_superuser or obj.id == request.user.id))

        if request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)

        return bool(request.user and (request.user.is_superuser or obj.id == request.user.id))