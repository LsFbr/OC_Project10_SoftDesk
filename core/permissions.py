# core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.models import Project, Issue, Comment, Contributor

def _user_is_contributor(user, project_id: int) -> bool:
    return Contributor.objects.filter(project_id=project_id, user=user).exists()

class IsProjectContributor(BasePermission):
    """
    Autorise l’accès aux ressources d’un projet uniquement à ses contributeurs.
    Laisse la création de projet ouverte aux utilisateurs authentifiés.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser: # si l'utilisateur est un superutilisateur, on lui donne accès à tout
            return True

        # Laisser passer la création de projet
        if getattr(view, "basename", None) == "project" and request.method == "POST":
            return True

        project_pk = view.kwargs.get("project_pk")
        if project_pk:
            return _user_is_contributor(request.user, project_pk)

        return True

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True

        if isinstance(obj, Project):
            project_id = obj.id
        elif isinstance(obj, Issue):
            project_id = obj.project_id
        elif isinstance(obj, Comment):
            project_id = obj.issue.project_id
        else:
            return False
        return _user_is_contributor(request.user, project_id)

class IsAuthorOrReadOnly(BasePermission):
    """Écriture réservée à l’auteur, lecture pour tous les contributeurs."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS: # si la méthode est safe (GET, OPTIONS, HEAD), on lui donne accès
            return True
        return getattr(obj, "author", None) == request.user # si l'objet a un auteur et que c'est l'utilisateur, on lui donne accès


class IsProjectAuthorForContributors(BasePermission):
    """
    Autorise POST/DELETE sur /projects/{pk}/contributors/ seulement à l’auteur du projet.
    Lecture autorisée aux contributeurs (gérée par IsProjectContributor).
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True

        # On ne restreint que les méthodes d'écriture
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            project_id = view.kwargs.get("project_pk")
            if not project_id:
                return False
            try:
                project = Project.objects.only("id", "author_id").get(id=project_id)
            except Project.DoesNotExist:
                return False
            return project.author_id == request.user.id
        return True
