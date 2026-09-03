from django.urls import include, path

urlpatterns = [
    path("", include("filter_site.urls")),
]
