from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    type = models.CharField(max_length=10)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
    )


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    project_id = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors"
    )
    role = models.CharField(max_length=20)


class Issue(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE, default=None)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=2000)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    # issue = models.ForeignKey()
    created_time = models.DateTimeField(auto_now_add=True)
