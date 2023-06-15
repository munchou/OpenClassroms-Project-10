from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet, ContributorViewSet
from users.views import MyObtainTokenPairView, NewUserView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="Project")
# router.register(r"projects/(<pk>)/users", ContributorViewSet, basename="Contributors")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", MyObtainTokenPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", NewUserView.as_view(), name="signup"),
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
    path("", include(router.urls)),
]

"""
URLS to set
/signup/
/login/
/projects/ (GET list all projects / POST create a project)
/projects/{id}/ (GET details of a project via its id / PUT to update a project / DELETE)
/projects/{id}/users/ (POST to link existing users to the project = contributor / GET the list of the contributors linked to that project)
/projects/{id}/users/{id} (REMOVE a contributor from a project)
/projects/{id}/issues/ (GET the list of the issues related to the project / POST create an issue related to the project)
/projects/{id}/issues/{id}/ (PUT update the issue / DELETE the issue)
/projects/{id}/issues/{id}/comments/ (POST create comments about an issue / GET list of the comments related to the issue)
/projects/{id}/issues/{id}/comments/{id}/ (PUT update the comment / DELETE delete the comment / GET show the comment)
"""
