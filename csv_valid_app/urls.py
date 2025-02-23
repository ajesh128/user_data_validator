# myapp/urls.py
from django.urls import path, include
from .views import UploadCsv


urlpatterns = [
    path("csv",UploadCsv.as_view(),name="csv")]
