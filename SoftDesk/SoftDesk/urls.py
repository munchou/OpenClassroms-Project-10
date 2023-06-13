from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet
from users.views import MyObtainTokenPairView, NewUserView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="Project")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", MyObtainTokenPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", NewUserView.as_view(), name="signup"),
    path("", include(router.urls)),
]
