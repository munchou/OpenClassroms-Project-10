from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    ProjectSerializer,
    ProjectSerializerGet,
    ContributorSerializer,
    ContributorSerializerGet,
    IssueSerializer,
    IssueSerializerGet,
    CommentSerializer,
    CommentSerializerGet,
)
from .permissions import (
    ProjectAuthor,
    ProjectAuthorOrContributor,
    IssueAuthor,
    CommentAuthor,
)
from .models import Project, Contributor, Issue, Comment


class ProjectViewSet(ModelViewSet):
    # queryset = Project.objects.all()
    # serializer_class = ProjectSerializerGet

    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if (
            self.action == "list"
            or self.action == "create"
            or self.action == "retrieve"
        ):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ProjectAuthor]
        return [permission() for permission in permission_classes]

    def list(self, request):
        projects = Project.objects.all()
        project = self.request.GET.get("project")
        if project is not None:
            projects = projects.filter(project=project)
        serializer = ProjectSerializerGet(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        copied_data = request.data.copy()
        copied_data["author"] = request.user.id

        types = ["back-end", "front-end", "ios", "android"]
        copied_data["type"] = copied_data["type"].casefold()
        if copied_data["type"] not in types:
            return Response("Available types : back-end, front-end, ios, android")

        serializer = ProjectSerializer(data=copied_data)

        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                user=request.user, project=project, role="author"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializerGet(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        copied_data = request.data.copy()
        copied_data["author"] = project.author.id

        types = ["back-end", "front-end", "ios", "android"]
        copied_data["type"] = copied_data["type"].casefold()
        if copied_data["type"] not in types:
            return Response("Available types : back-end, front-end, ios, android")

        serializer = ProjectSerializer(project, data=copied_data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user == project.author:
            project.delete()
            return Response(
                f"Project (ID: {pk}) deleted.", status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            "Only the author of the project can delete it.",
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all().select_related("project")
    serializer_class = ContributorSerializerGet

    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ProjectAuthor]
        return [permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("projects_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response("That project does not exist")
        return self.queryset.filter(project=project)

    def create(self, request, *args, **kwargs):
        project_pk = self.kwargs.get("projects_pk")

        copied_data = request.data.copy()
        copied_data["project"] = project_pk
        copied_data["role"] = "contributor"

        try:
            contributor = Contributor.objects.get(
                user=copied_data["user"], project=project_pk
            )
            return Response(
                f"[{contributor.user}] (ID: {contributor.user} is already part of the project.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Contributor.DoesNotExist:
            try:
                user = get_object_or_404(User, id=copied_data["user"])
                # user = User.objects.get(id=copied_data["user"])
                serializer = ContributorSerializer(data=copied_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        f"[{user.username}] was added successfully.",
                        status=status.HTTP_201_CREATED,
                    )
                print(f"ERRORS {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(f"That user does not exist.")

    def destroy(self, request, *args, **kwargs):
        project_pk = self.kwargs.get("projects_pk")
        contributor_pk = self.kwargs.get("pk")
        contributor = get_object_or_404(
            Contributor, user=contributor_pk, project=project_pk
        )

        if contributor.role == "author":
            return Response(
                f"{contributor.user} (ID: {contributor_pk}) cannot be deleted as they are the author of the project.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        contributor.delete()
        return Response(
            f"{contributor.user} is no longer a contributor of the project.",
            status=status.HTTP_202_ACCEPTED,
        )


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all().select_related("project")
    serializer_class = IssueSerializerGet

    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if self.action == "list" or self.action == "create":
            permission_classes = [ProjectAuthorOrContributor]
        else:
            permission_classes = [IssueAuthor]
        return [permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("projects_pk")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response("That project does not exist")
        return self.queryset.get(project=project)

    def create(self, request, *args, **kwargs):
        project_pk = self.kwargs.get("projects_pk")

        copied_data = request.data.copy()
        copied_data["project"] = project_pk
        copied_data["author"] = request.user.id

        print(f"\nrequest.user.id {request.user.id}\n")

        if copied_data["assignee"] == "":
            copied_data["assignee"] = request.user.id

        try:
            contributor = get_object_or_404(
                Contributor, user=copied_data["assignee"], project=project_pk
            )
            copied_data["assignee"] = contributor.id
        except Exception:
            pass

        try:
            Contributor.objects.get(id=copied_data["assignee"], project=project_pk)
            serializer = IssueSerializer(data=copied_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response(
                f"User_id:{copied_data['assignee']} is either not a contributor or does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        project_pk = self.kwargs.get("projects_pk")
        issue_pk = self.kwargs.get("pk")

        issue = get_object_or_404(Issue, id=issue_pk)
        copied_data = request.data.copy()
        copied_data["tag"] = issue.tag
        copied_data["project"] = issue.project.id
        copied_data["author"] = issue.author.id
        # copied_data["assignee"] = issue.assignee.id

        if copied_data["assignee"] == "":
            copied_data["assignee"] = request.user.id

        try:
            contributor = get_object_or_404(
                Contributor, user=copied_data["assignee"], project=project_pk
            )
            copied_data["assignee"] = contributor.id
        except Exception:
            pass

        try:
            Contributor.objects.get(id=copied_data["assignee"], project=project_pk)
            serializer = IssueSerializer(issue, data=copied_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response(
                f"User_id:{copied_data['assignee']} is either not a contributor or does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        issue_pk = self.kwargs.get("pk")
        issue = get_object_or_404(Issue, id=issue_pk)

        issue.delete()
        return Response(
            "The issue was delete successfully.", status=status.HTTP_202_ACCEPTED
        )


class CommentViewSet(ModelViewSet):
    # queryset = Comment.objects.all().select_related("isuues")
    # serializer_class = CommentSerializer

    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "create"
        ):
            permission_classes = [ProjectAuthorOrContributor]
        else:
            permission_classes = [CommentAuthor]
        return [permission() for permission in permission_classes]

    def list(self, request, projects_pk, pk):
        # issue = Issue.objects.get(id=issue_pk)
        issue = get_object_or_404(Issue, id=pk)
        comments = Comment.objects.filter(issue_id=issue)
        serializer = CommentSerializerGet(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, projects_pk, pk):
        # project = get_object_or_404(Project, id=projects_pk)
        issue = get_object_or_404(Issue, id=pk)
        print(f"\nISSUE ID {issue.id}\n")
        copied_data = request.data.copy()
        copied_data["issue_id"] = issue.id
        copied_data["author"] = request.user.id

        serializer = CommentSerializer(data=copied_data)
        print(f"\nSERiALIZER {serializer}\n")
        if serializer.is_valid():
            print("\nVALIDATOR OK\n")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("\nVALIDATOR NOOOOOOOT OK\n")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, projects_pk, pk, comment_pk):
        # project = get_object_or_404(Project, id=projects_pk)
        # issue = get_object_or_404(Issue, id=pk)
        comment = get_object_or_404(Comment, id=comment_pk)
        copied_data = request.data.copy()
        copied_data["issue_id"] = comment.issue_id.id
        copied_data["author"] = comment.author.id

        serializer = CommentSerializer(comment, data=copied_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, projects_pk, pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializerGet(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, projects_pk, pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)

        if request.user == comment.author:
            comment.delete()
            return Response(
                "The comment was delete successfully.", status=status.HTTP_202_ACCEPTED
            )

        return Response(
            "Only the author of the comment can delete that comment.",
            status=status.HTTP_400_BAD_REQUEST,
        )
