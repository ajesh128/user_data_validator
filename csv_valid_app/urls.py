# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReadCSVView


# router.register(r'csv1',ReadCSVView)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path("csv/",include(router.urls))
# ]

urlpatterns = [
    path("read-csv",ReadCSVView.as_view(),name="csv")]
