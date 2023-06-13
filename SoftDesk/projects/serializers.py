from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    # To display the author's name instead of their ID
    author = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ["title", "description", "type", "author"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project_id", "role"]


class IssueSerializer(serializers.ModelSerializer):
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["description", "author", "created_time"]
