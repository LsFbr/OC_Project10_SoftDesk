from django.contrib import admin
from core.models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "type", "author", "created_time")


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "created_time")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "description", "tag", "priority", "status",
        "project", "author", "assignee", "created_time"
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "issue", "author", "created_time")
