from django.urls import path
from .views import UploadCSVView, DatasetHistoryView

urlpatterns = [
    path("upload/", UploadCSVView.as_view(), name="upload_csv"),
    path("history/", DatasetHistoryView.as_view(), name="dataset_history"),
]
