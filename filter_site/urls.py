from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/predict", views.predict_api, name="predict_api"),
    path("api/predict/<str:job_id>", views.prediction_status, name="prediction_status"),
]
