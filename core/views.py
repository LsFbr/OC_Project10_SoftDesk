# core/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, PermissionDenied, MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.models import Contributor, Project, Issue, Comment
from core.serializers import (
    ProjectListSerializer, ProjectDetailSerializer,
    ContributorListSerializer, ContributorDetailSerializer,
    IssueListSerializer, IssueDetailSerializer,
    CommentListSerializer, CommentDetailSerializer
)
from core.permissions import IsProjectContributor, IsAuthorOrReadOnly, IsProjectAuthorForContributors


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.detail_serializer_class and getattr(self, "action", None) in (
            "retrieve", "create", "update", "partial_update"
        ):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all() # si l'utilisateur est un superutilisateur, on lui donne accès à tous les projets
        return Project.objects.filter(contributors__user=user) # filtre les projets dont l'utilisateur est contributeur

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user) # crée un projet et l'associe à l'utilisateur en tant que créateur
        Contributor.objects.get_or_create(user=self.request.user, project=project) # crée un contributeur pour le projet

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # récupère le projet à supprimer
        project_id = instance.id # récupère l'id du projet
        title = instance.title # récupère le titre du projet

        self.perform_destroy(instance) # supprime le projet

        return Response({"detail": f"Project '{title}' (id={project_id}) deleted."}, status=status.HTTP_200_OK) # renvoie une réponse de succès


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthorForContributors]

    def get_queryset(self):
        # /projects/{project_pk}/contributors/
        project_id = self.kwargs.get('project_pk')
        queryset = Contributor.objects.select_related("user", "project")
        return queryset.filter(project_id=project_id) if project_id else queryset.none()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if not project_id:
            raise ValidationError("Project context is required.")
        user = serializer.validated_data.get("user")
        if Contributor.objects.filter(project_id=project_id, user=user).exists():
            raise ValidationError("This user is already a contributor of the project.")
        serializer.save(project_id=project_id)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id == instance.project.author_id:
            raise PermissionDenied("You cannot remove the project's author from contributors.")

        contributor_id = instance.id
        username = instance.user.username
        project_id = instance.project_id
        project_title = instance.project.title

        self.perform_destroy(instance)

        return Response(
            {"detail": f"Contributor '{username}'(id={contributor_id}) removed from project '{project_title}' (id={project_id})."},
            status=status.HTTP_200_OK
        )


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        # /projects/{project_pk}/issues/
        project_id = self.kwargs.get('project_pk')
        queryset = Issue.objects.select_related("author", "assignee", "project")
        return queryset.filter(project_id=project_id) if project_id else queryset.none()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if not project_id:
            raise ValidationError("Project context is required.")

        assignee = serializer.validated_data.get("assignee")
        if assignee is None:
            assignee = self.request.user

        serializer.save(project_id=project_id, author=self.request.user, assignee=assignee)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        issue_id = instance.id
        title = instance.title
        project_id = instance.project_id
        project_title = instance.project.title
        
        self.perform_destroy(instance)

        return Response(
            {"detail": f"Issue '{title}' (id={issue_id}) deleted from project '{project_title}' (id={project_id})."},
            status=status.HTTP_200_OK
        )


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        # /projects/{project_pk}/issues/{issue_pk}/comments/
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')
        queryset = Comment.objects.select_related("author", "issue", "issue__project")
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        if project_id:
            queryset = queryset.filter(issue__project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')
        if not issue_id:
            raise ValidationError("Issue context is required.")
        try:
            issue = Issue.objects.get(id=issue_id, project_id=project_id)
        except Issue.DoesNotExist:
            raise ValidationError("Issue not found for this project.")
        serializer.save(issue=issue, author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        comment_id = instance.id
        description = instance.description
        issue_id = instance.issue_id
        issue_title = instance.issue.title

        self.perform_destroy(instance)
        
        return Response(
            {"detail": f"Comment '{description}' (id={comment_id}) deleted from issue '{issue_title}' (id={issue_id})."},
            status=status.HTTP_200_OK
        )
