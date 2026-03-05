from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import include, path


def hello_world(request: HttpRequest):
    name = request.GET.get("name", "World")

    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('hello/', hello_world),
    path("user/", include("hexagonal.urls")),
    # path('',include("week2.urls"))
    path("", include("week3.urls")),
]
