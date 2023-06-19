from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from projects.views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)
from users.views import NewUserView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenBlacklistView,
)


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="Project")


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("login/", MyObtainTokenPairView.as_view(), name="login"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", NewUserView.as_view(), name="signup"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "projects/<int:pk>/users/",
        ContributorViewSet.as_view(
            {"get": "retrieve", "post": "create", "delete": "destroy"}
        ),
        name="contributors",
    ),
    path(
        "projects/<int:pk>/users/<int:contributor_pk>/",
        ContributorViewSet.as_view({"delete": "destroy"}),
        name="contributors_delete",
    ),
    path(
        "projects/<int:pk>/issues/",
        IssueViewSet.as_view({"get": "list", "post": "create"}),
        name="issues",
    ),
    path(
        "projects/<int:pk>/issues/<int:issue_pk>/",
        IssueViewSet.as_view({"put": "update", "delete": "destroy"}),
        name="issues_edit",
    ),
    path(
        "projects/<int:pk>/issues/<int:issue_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments",
    ),
    path(
        "projects/<int:pk>/issues/<int:issue_pk>/comments/<int:comment_pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="comments_edit",
    ),
    path("", include(router.urls)),
]
