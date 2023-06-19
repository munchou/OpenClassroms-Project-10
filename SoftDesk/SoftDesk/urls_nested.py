from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from projects.views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)
from users.views import MyObtainTokenPairView, NewUserView

from rest_framework_simplejwt.views import TokenRefreshView


router = SimpleRouter()

router.register("projects", ProjectViewSet, basename="projects")
projects_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
projects_router.register(r"projects", ProjectViewSet, basename="projects")

router.register("issues", IssueViewSet, basename="issues")
# router.register("comments", CommentViewSet, basename="comments")

users_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
users_router.register(r"users", ContributorViewSet, basename="projects-users")

issues_router = routers.NestedSimpleRouter(router, r"projects", lookup="projects")
issues_router.register(r"issues", IssueViewSet, basename="projects-issues")

# comments_router = routers.NestedSimpleRouter(router, r"issues", lookup="issues")
# comments_router.register(r"comments", CommentViewSet, basename="issues-comments")

app_name = "projects"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include(users_router.urls)),
    path("", include(issues_router.urls)),
    path(
        "projects/<int:projects_pk>/issues/<int:pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments",
    ),
    path(
        "projects/<int:projects_pk>/issues/<int:pk>/comments/<int:comment_pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="comments_edit",
    ),
    # path("", include(comments_router.urls)),
    path("login/", MyObtainTokenPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", NewUserView.as_view(), name="signup"),
]
