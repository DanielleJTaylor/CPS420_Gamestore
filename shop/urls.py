from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as catalog_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # login
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),

    # use YOUR logout_view (allows GET)
    path("logout/", catalog_views.logout_view, name="logout"),

    # signup
    path("signup/", catalog_views.signup_view, name="signup"),

    # catalog
    path("", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
