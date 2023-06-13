from rest_framework.serializers import ModelSerializer

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description", "type", "author"]


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project_id", "role"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "title",
            "desc",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "created_time",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["description", "author", "created_time"]
