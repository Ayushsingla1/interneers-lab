from django.urls import path
from . import composition_root

urlpatterns = [
     path('create/',composition_root.user_controller.request_handler)
]

