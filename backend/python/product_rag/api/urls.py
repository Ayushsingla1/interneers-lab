from django.urls import path

from ..composition_root import agent_upload, agent_query

urlpatterns = [
    path("agent/upload/", agent_upload, name="agent-upload"),
    path("agent/query/", agent_query, name="agent-query"),
]
