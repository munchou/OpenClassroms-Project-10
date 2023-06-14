from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import (
    ProjectSerializer,
    ProjectSerializerGet,
    ContributorSerializer,
    IssueSerializer,
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
    #     project_id = self.request.GET.get("project_id")
    #     if project_id is not None:
    #         projects = projects.filter(project_id=project_id)
    #     serializer = ProjectSerializerGet(projects, many=True)
    #     return Response(serializer.data)

    def list(self, request):
        projects = Project.objects.all()
        project_id = self.request.GET.get("project_id")
        if project_id is not None:
            projects = projects.filter(project_id=project_id)
        serializer = ProjectSerializerGet(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        copied_data = request.data.copy()
        # request.user get the author status linked to that project
        copied_data["author"] = request.user.id
        serializer = ProjectSerializer(data=copied_data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                user=request.user, project_id=project, role="author"
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

    def detroy(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(
            f"Project (ID: {pk}) deleted.", status=status.HTTP_204_NO_CONTENT
        )


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
