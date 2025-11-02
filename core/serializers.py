from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from core.models import Contributor, Project, Issue, Comment

User = get_user_model()

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author", "created_time", "issues", "contributors"]
        read_only_fields = ["id", "author", "created_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        data["contributors"] = [{"id": contributor.id, "user": contributor.user.username} for contributor in instance.contributors.all()]
        data["issues"] = [{"id": issue.id, "title": issue.title} for issue in instance.issues.all()]
        return data


class ContributorListSerializer(ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ["id", "user", "created_time"]
        read_only_fields = ["id", "created_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = {"id": instance.user_id, "username": instance.user.username}
        return data


class ContributorDetailSerializer(ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["id", "created_time", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = {"id": instance.user_id, "username": instance.user.username}
        data["project"] = {"id": instance.project_id, "title": instance.project.title}
        return data


class IssueListSerializer(ModelSerializer):

    description = serializers.CharField(write_only=True, required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Issue
        fields = ["id", "title", "tag", "priority", "status", "author", "created_time", "description", "assignee"]
        read_only_fields = ["id", "author", "created_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        return data

    def validate_assignee(self, value):
        if value is None:
            return value
        view = self.context.get("view")
        project_id = None
        if view:
            project_id = view.kwargs.get("project_pk")
        if project_id is None and self.instance is not None:
            project_id = self.instance.project_id
        if project_id and not Contributor.objects.filter(project_id=project_id, user=value).exists():
            raise serializers.ValidationError("L'utilisateur doit être contributor du projet.")
        return value

class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "tag", "priority", "status", "project", "author", "assignee", "created_time", "comments"]
        read_only_fields = ["id", "author", "created_time", "project"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        data["project"] = {"id": instance.project_id, "title": instance.project.title}
        if instance.assignee:
            data["assignee"] = {"id": instance.assignee_id, "username": instance.assignee.username}
        else:
            data["assignee"] = None
        data["comments"] = [{"id": comment.id, "description": comment.description} for comment in instance.comments.all()]
        return data


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        return data


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "issue", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time", "issue"]

    def to_representation(self, instance):
        request = self.context.get("request")
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        data["issue"] = {
            "id": instance.issue_id, 
            "title": instance.issue.title,
            "url": request.build_absolute_uri(
                reverse(
                    "project-issues-detail",
                    kwargs={"project_pk": instance.issue.project_id, "pk": instance.issue_id},
                    request=request,
                )
            )
        }
        return data

