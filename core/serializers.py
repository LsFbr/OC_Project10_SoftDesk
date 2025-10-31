from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
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
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, allow_null=True)

    class Meta:
        model = Issue
        fields = ["id", "title", "tag", "priority", "status", "author", "created_time", "description", "assignee"]
        read_only_fields = ["id", "author", "created_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = {"id": instance.author_id, "username": instance.author.username}
        return data

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
        return data

class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time", "issue"]

class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description", "issue", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time", "issue"]

