import uuid
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    class Type(models.TextChoices):
        BACKEND = "BACKEND", "Back-end"
        FRONTEND = "FRONTEND", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_projects")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    class Role(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CONTRIBUTOR = "CONTRIBUTOR", "Contributor"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    role = models.CharField(max_length=20, choices=Role.choices)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user} → {self.project} ({self.role})"


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = "BUG", "Bug"
        FEATURE = "FEATURE", "Feature"
        TASK = "TASK", "Task"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Status(models.TextChoices):
        TODO = "TODO", "To do"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        FINISHED = "FINISHED", "Finished"

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=20, choices=Tag.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_issues")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_issues", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.project}] {self.title}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=2048)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_comments")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on {self.issue}"
