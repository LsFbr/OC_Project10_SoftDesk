import uuid
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    PROJECT_TYPES = [
        ('BE', 'Back-end'),
        ('FE', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="authored_projects")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title


class Contributor(models.Model):

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name="contributors")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "project"], name="uniq_user_project")
        ]
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.user} → {self.project}"


class Issue(models.Model):
    TAGS = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    PRIORITIES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    STATUSES = [
        ('TODO', 'To do'),
        ('IN_PROGRESS', 'In progress'),
        ('FINISHED', 'Finished'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=20, choices=TAGS)
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    status = models.CharField(max_length=20, choices=STATUSES, default="TODO")
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="authored_issues")
    assignee = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        related_name="assigned_issues", null=True, blank=True
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"[{self.project}] {self.title}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=2048)
    issue = models.ForeignKey('core.Issue', on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="authored_comments")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"Comment {self.id} on {self.issue}"
