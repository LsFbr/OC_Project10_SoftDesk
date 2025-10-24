from rest_framework.viewsets import ModelViewSet
from core.models import Contributor, Project, Issue, Comment
from core.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

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
        Contributor.objects.get_or_create(
            user=self.request.user,
            project=project,
            defaults={'role': 'AUTHOR'}
        )



class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
