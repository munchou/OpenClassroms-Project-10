from django.contrib.auth.models import User

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import (
    ProjectSerializer,
    ProjectSerializerGet,
    ContributorSerializer,
    ContributorSerializerGet,
    IssueSerializer,
    IssueSerializerGet,
    CommentSerializer,
)
from .permissions import IsAuthor, IsContributor
from .models import Project, Contributor, Issue, Comment


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     projects = Project.objects.all()
    #     project = self.request.GET.get("project")
    #     if project is not None:
    #         projects = projects.filter(project=project)
    #     serializer = ProjectSerializerGet(projects, many=True)
    #     return Response(serializer.data)

    def list(self, request):
        projects = Project.objects.all()
        project = self.request.GET.get("project")
        if project is not None:
            projects = projects.filter(project=project)
        serializer = ProjectSerializerGet(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        copied_data = request.data.copy()
        # request.user is given the author status linked to that project
        copied_data["author"] = request.user.id
        serializer = ProjectSerializer(data=copied_data)

        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                user=request.user, project=project, role="author"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializerGet(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        copied_data = request.data.copy()
        copied_data["author"] = project.author.id
        serializer = ProjectSerializer(project, data=copied_data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(
            f"Project (ID: {pk}) deleted.", status=status.HTTP_204_NO_CONTENT
        )


class ContributorViewSet(ModelViewSet):
    # queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        users = Contributor.objects.filter(project=project)
        serializer = ContributorSerializerGet(users, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        copied_data = request.data.copy()
        copied_data["project"] = project.id
        copied_data["role"] = "contributor"

        try:
            # Contributor.objects.get(user=copied_data["user"], project=project.id)
            contributor = Contributor.objects.get(
                user=copied_data["user"], project=project.id
            )
            return Response(
                f"[{contributor.user}] (ID: {contributor.user} is already part of the project.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Contributor.DoesNotExist:
            try:
                user = User.objects.get(id=copied_data["user"])
                serializer = ContributorSerializer(data=copied_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        f"[{user.username}] was added successfully.",
                        status=status.HTTP_201_CREATED,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(f"That user does not exist.")

    def destroy(self, request, pk, contributor_pk):
        # project = Project.objects.get(pk=pk)
        # contributor = Contributor.objects.get(user=contributor_pk)
        # project = get_object_or_404(Project, pk=pk)
        contributor = get_object_or_404(Contributor, user=contributor_pk)

        if contributor.role == "author":
            return Response(
                f"{contributor.user} (ID: {contributor_pk}) cannot be deleted as they are the author of the project."
            )

        contributor.delete()
        return Response(
            f"{contributor.user} is no longer a contributor of the project."
        )


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer()
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        issues = Issue.objects.filter(project=project)
        serializer = IssueSerializerGet(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        copied_data = request.data.copy()
        copied_data["project"] = project.id
        copied_data["author"] = request.user.id

        # print(f"\nPROJECT ID {project.id}\n")
        # contributors = Contributor.objects.all()
        # print(f"\nUSERTEST {contributors}\n")
        # test = Contributor.objects.get(id=8)
        # print(f"\nCONTRIBUTOR TEST {test.user}\n")
        # user = get_object_or_404(User, id=copied_data["assignee"])
        # print(f"\nUSER {user}\n")

        try:
            Contributor.objects.get(id=copied_data["assignee"], project=project.id)
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

    # def update(self, request, pk=None):
    #     project = Project.objects.get(pk=pk)
    #     copied_data = request.data.copy()
    #     copied_data["author"] = project.author.id
    #     serializer = ProjectSerializer(project, data=copied_data)
    #     if serializer.is_valid(raise_exception=True):
    #         project = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk=None):
    #     pass
    # project = Project.objects.get(pk=pk)
    # project.delete()
    # return Response(
    #     f"Project (ID: {pk}) deleted.", status=status.HTTP_204_NO_CONTENT
    # )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer()
    permission_classes = (IsAuthenticated,)
