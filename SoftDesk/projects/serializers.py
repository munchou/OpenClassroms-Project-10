from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Project, Contributor, Issue, Comment


class ProjectSerializerGet(serializers.ModelSerializer):
    # To display the author's name instead of their ID
    author = serializers.StringRelatedField(read_only=True)

    title = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Project.objects.all())]
    )

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Project.objects.all())]
    )

    class Meta:
        model = Project
        fields = ["title", "description", "type", "author"]


class ContributorSerializerGet(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ["user", "project", "role"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project", "role"]


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
