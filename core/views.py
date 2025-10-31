from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from core.models import Contributor, Project, Issue, Comment
from core.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, ContributorDetailSerializer, IssueSerializer, CommentSerializer

class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.get_or_create(user=self.request.user, project=project)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_id = instance.id
        title = instance.title

        self.perform_destroy(instance)

        return Response(
            {
                "detail": f"Project '{title}' (id={project_id}) deleted.",
            },
            status=status.HTTP_200_OK
        )


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        # /projects/{project_pk}/contributors/
        project_id = self.kwargs.get('project_pk')
        queryset = Contributor.objects.select_related("user", "project")
        return queryset.filter(project_id=project_id) if project_id else queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        if not project_id:
            raise ValidationError("Project context is required.")
        user = serializer.validated_data.get("user")
        if Contributor.objects.filter(project_id=project_id, user=user).exists():
            raise ValidationError("This user is already a contributor of the project.")
        serializer.save(project_id=project_id) 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        contributor_id = instance.id
        username = instance.user.username
        project_id = instance.project_id
        project_title = instance.project.title

        self.perform_destroy(instance)

        return Response(
            {
                "detail": f"Contributor '{username}'(id={contributor_id}) removed from project '{project_title}' (id={project_id}).",
            },
            status=status.HTTP_200_OK
        )


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
