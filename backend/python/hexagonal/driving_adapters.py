from . import service, driving_ports
from django.http import HttpRequest, HttpResponse

class UserController:

    def __init__(self,create_user_service : service.CreateUserService):
        self.create_user_service = create_user_service
    
    def request_handler(self,request : HttpRequest):

        try:
            user = self.create_user_service.execute(driving_ports.CreateUser(request.GET.get("name","cristiano"),request.GET.get("email","random@gmail.com")))
            return HttpResponse(b"User created successfully")
        except:
            return HttpResponse(b"User already exists", status=409)
    
