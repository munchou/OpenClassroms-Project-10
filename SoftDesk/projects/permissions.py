from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.generics import get_object_or_404

from .models import Project, Contributor, Issue, Comment


class ProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs["pk"])

        return bool(project.author == request.user)


class ProjectAuthorOrContributor(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs["pk"])

        try:
            contributor = get_object_or_404(
                Contributor, user=request.user, project=project.id
            )
        except Contributor.DoesNotExist:
            return False

        # print(f"\nREQUEST USER: {request.user.id}")
        # print(f"PROJECT AUTHOR: {project.author}\n")
        # print(f"CONTRIBUTOR OBJECTS: {contributor}\n")

        return bool(
            request.user
            and (project.author == request.user or contributor == request.user)
        )


class IssueAuthor(BasePermission):
    def has_permission(self, request, view):
        issue = get_object_or_404(Issue, id=view.kwargs["issue_pk"])

        return bool(request.user and issue.author == request.user)


class CommentAuthor(BasePermission):
    def has_permission(self, request, view):
        comment = get_object_or_404(Comment, id=view.kwargs["comment_pk"])

        return bool(request.user and comment.author == request.user)
