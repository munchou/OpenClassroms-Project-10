from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Project.objects.all())]
    )

    class Meta:
        model = Project
        fields = ["title", "description", "type", "author"]


class ProjectSerializerGet(serializers.ModelSerializer):
    # To display the author's name instead of their ID
    author = serializers.StringRelatedField(read_only=True)

    title = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Project.objects.all())]
    )

    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]


class ContributorSerializerGet(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "role"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "role"]


class IssueSerializerGet(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    assignee = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "desc",
            "tag",
            "priority",
            "project",
            "status",
            "author",
            "assignee",
            "created_time",
        ]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "desc",
            "tag",
            "priority",
            "project",
            "status",
            "author",
            "assignee",
            "created_time",
        ]


class CommentSerializerGet(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue_id", "created_time"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue_id", "created_time"]
