from django.urls import path

from .views import CreateUploadView

urlpatterns = [path("uploads/", CreateUploadView.as_view(), name="file-upload-create")]
