from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Project(models.Model):
    TYPE = [
        ("back-end", "BACK-END"),
        ("front-end", "FRONT-END"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    type = models.CharField(max_length=9, choices=TYPE)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
    )

    def __str__(self):
        return f"{self.title} by {self.author} [{self.type}] | ID: {self.id}"


class Contributor(models.Model):
    ROLE = [("author", "AUTHOR"), ("contributor", "CONTRIBUTOR")]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors"
    )
    role = models.CharField(max_length=11, choices=ROLE)

    def __str__(self):
        return f"{self.user} (ID: {self.user.id}) | {self.project} | {self.role}"


class Issue(models.Model):
    TAG = [("bug", "BUG"), ("improvement", "IMPROVEMENT"), ("task", "TASK")]
    PRIORITY = [("low", "LOW"), ("moderate", "MODERATE"), ("high", "HIGH")]
    STATUS = [
        ("to_do", "TO DO"),
        ("in_progress", "IN PROGRESS"),
        ("completed", "COMPLETED"),
    ]

    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    tag = models.CharField(max_length=11, choices=TAG)
    priority = models.CharField(max_length=8, choices=PRIORITY)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=11, choices=STATUS)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE, default=None)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.priority} priority] {self.title} by {self.author}, [{self.tag}]"


class Comment(models.Model):
    description = models.CharField(max_length=2000)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE, default=None)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author}, issue id {self.issue_id}"
