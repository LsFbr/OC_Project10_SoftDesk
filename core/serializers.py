from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Contributor, Project, Issue, Comment


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]


class ProjectDetailSerializer(ModelSerializer):

    contributors = SerializerMethodField()
    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author", "created_time", "issues", "contributors"]
        read_only_fields = ["id", "author", "created_time"]

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        return [{"id": contributor.id, "user": contributor.user.username} for contributor in queryset]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        return [{"id": issue.id, "title": issue.title} for issue in queryset]

class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "role", "created_time"]
        read_only_fields = ["id", "created_time"]


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "tag", "priority", "status", "project", "author", "assignee", "created_time", "comments"]
        read_only_fields = ["id", "author", "created_time"]

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "issue", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]

