from django.urls import path

from ..composition_root import upload_doc, query_doc

urlpatterns = [
    path("upload/", upload_doc, name="upload"),
    path("query/", query_doc, name="query"),
]
