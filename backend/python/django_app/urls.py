from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpRequest

def hello_world(request : HttpRequest):
   name = request.GET.get("name","World")

   return JsonResponse({"message" : f"Hello, {name}!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', hello_world),
    path('user/', include("hexagonal.urls")),
    path('',include("week2.urls"))
]
