from django.contrib.auth.models import User
from django.db.models import Q

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
        if self.action == "create" or self.action == "list":
            permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            permission_classes = [ProjectAuthorOrContributor]
        else:
            permission_classes = [ProjectAuthor]
        return [permission() for permission in permission_classes]

    def list(self, request):
        # projects = Project.objects.all()
        project = self.request.GET.get("project")
        projects = Project.objects.filter(
            Q(contributors__user=request.user) | Q(author=request.user)
        )
        print(f"\n PROJECTS CONTRIBUTORS: ({len(projects)}) {projects}")

        try:
            if project is not None:
                projects = projects.filter(project=project)
            serializer = ProjectSerializerGet(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                "You are not linked to any project.",
                status=status.HTTP_400_BAD_REQUEST,
            )

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
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            return Response(
                "Available types : back-end, front-end, ios, android",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProjectSerializer(project, data=copied_data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user == project.author:
            project.delete()
            return Response(f"Project (ID: {pk}) deleted.", status=status.HTTP_200_OK)
        return Response(
            "Only the author of the project can delete it.",
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContributorViewSet(ModelViewSet):
    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ProjectAuthor]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        users = Contributor.objects.filter(project=project)
        serializer = ContributorSerializerGet(users, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        # project = Project.objects.get(pk=pk)
        project = get_object_or_404(Project, pk=pk)

        copied_data = request.data.copy()
        copied_data["project"] = project.id
        copied_data["role"] = "contributor"

        try:
            contributor = Contributor.objects.get(
                user=copied_data["user"], project=project.id
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
                return Response(
                    f"That user does not exist.", status=status.HTTP_400_BAD_REQUEST
                )

    def destroy(self, request, pk, contributor_pk):
        contributor = get_object_or_404(Contributor, user=contributor_pk, project=pk)

        if contributor.role == "author":
            return Response(
                f"{contributor.user} (ID: {contributor_pk}) cannot be deleted as they are the author of the project.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        contributor.delete()
        return Response(
            f"{contributor.user} is no longer a contributor of the project.",
            status=status.HTTP_200_OK,
        )


class IssueViewSet(ModelViewSet):
    # queryset = Issue.objects.all().select_related("project")
    # serializer_class = IssueSerializerGet

    def get_permissions(self):
        """Instantiates and returns the list of
        permissions that this view requires."""
        if self.action == "list" or self.action == "create":
            permission_classes = [ProjectAuthorOrContributor]
        else:
            permission_classes = [IssueAuthor]
        return [permission() for permission in permission_classes]

    def list(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        issues = Issue.objects.filter(project=project)
        serializer = IssueSerializerGet(issues, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        project_id = project.id

        copied_data = request.data.copy()
        copied_data["project"] = project_id
        copied_data["author"] = request.user.id

        tags = ["bug", "improvement", "task"]
        copied_data["tag"] = copied_data["tag"].casefold()
        if copied_data["tag"] not in tags:
            return Response("Available tags : bug, improvement, task")

        priorities = ["low", "moderate", "high"]
        copied_data["priority"] = copied_data["priority"].casefold()
        if copied_data["priority"] not in priorities:
            return Response("Available priorities : low, moderate, high")

        status_list = ["to_do", "in_progress", "completed"]
        copied_data["status"] = copied_data["status"].casefold()
        if copied_data["status"] not in status_list:
            return Response("Available priorities : to_do, in_progress, completed")

        # ----------- Checking the "user" input
        project_contributors = Contributor.objects.filter(project=pk)
        contrib_users_list = []
        for contrib in project_contributors:
            contrib_users_list.append(contrib.user.username)

        user_input = copied_data["assignee"]
        if user_input.isdigit():
            pass
        elif user_input in contrib_users_list:
            picked_user = User.objects.get(username=user_input)
            copied_data["assignee"] = picked_user.id
        else:
            print(
                f"Blank input or user [{user_input}] does not exist, authenticated user [{request.user}] selected as assignee."
            )
            copied_data["assignee"] = request.user.id
        # ---------------------------------------------

        # if copied_data["assignee"] == "":
        #     copied_data["assignee"] = request.user.id

        try:
            contributor = get_object_or_404(
                Contributor, user=copied_data["assignee"], project=project_id
            )
            copied_data["assignee"] = contributor.id
        except Exception:
            pass

        try:
            Contributor.objects.get(id=copied_data["assignee"], project=project_id)
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

    def update(self, request, pk, issue_pk):
        project = get_object_or_404(Project, id=pk)
        project_id = project.id
        issue = get_object_or_404(Issue, id=issue_pk)
        copied_data = request.data.copy()
        copied_data["project"] = issue.project.id
        copied_data["author"] = issue.author.id

        tags = ["bug", "improvement", "task"]
        copied_data["tag"] = copied_data["tag"].casefold()
        if copied_data["tag"] not in tags:
            return Response("Available tags : bug, improvement, task")

        priorities = ["low", "moderate", "high"]
        copied_data["priority"] = copied_data["priority"].casefold()
        if copied_data["priority"] not in priorities:
            return Response("Available priorities : low, moderate, high")

        status_list = ["to_do", "in_progress", "completed"]
        copied_data["status"] = copied_data["status"].casefold()
        if copied_data["status"] not in status_list:
            return Response("Available priorities : to_do, in_progress, completed")

        # ----------- Checking the "user" input
        project_contributors = Contributor.objects.filter(project=pk)
        contrib_users_list = []
        for contrib in project_contributors:
            contrib_users_list.append(contrib.user.username)
        print(f"\n contrib_users_list: {request.user}\n")

        user_input = copied_data["assignee"]
        if user_input.isdigit():
            pass
        elif user_input in contrib_users_list:
            picked_user = User.objects.get(username=user_input)
            copied_data["assignee"] = picked_user.id
        else:
            print(
                f"Blank input or user [{user_input}] does not exist, authenticated user [{request.user}] selected as assignee."
            )
            copied_data["assignee"] = request.user.id
        # ---------------------------------------------

        # if copied_data["assignee"] == "":
        #     copied_data["assignee"] = request.user.id

        try:
            contributor = get_object_or_404(
                Contributor, user=copied_data["assignee"], project=project_id
            )
            copied_data["assignee"] = contributor.id
        except Exception:
            pass

        try:
            Contributor.objects.get(id=copied_data["assignee"], project=project_id)
            serializer = IssueSerializer(issue, data=copied_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response(
                f"User_id:{copied_data['assignee']} is either not a contributor or does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)
        # issue = Issue.objects.get(id=issue_pk)

        issue.delete()
        return Response("The issue was delete successfully.", status=status.HTTP_200_OK)


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

    def list(self, request, pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)
        comments = Comment.objects.filter(issue_id=issue)
        serializer = CommentSerializerGet(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk, issue_pk):
        issue = get_object_or_404(Issue, id=issue_pk)

        copied_data = request.data.copy()
        copied_data["issue_id"] = issue.id
        copied_data["author"] = request.user.id

        serializer = CommentSerializer(data=copied_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        copied_data = request.data.copy()
        copied_data["issue_id"] = comment.issue_id.id
        copied_data["author"] = comment.author.id

        serializer = CommentSerializer(comment, data=copied_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializerGet(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk, issue_pk, comment_pk):
        comment = get_object_or_404(Comment, id=comment_pk)

        comment.delete()
        return Response(
            "The comment was deleted successfully.", status=status.HTTP_200_OK
        )
