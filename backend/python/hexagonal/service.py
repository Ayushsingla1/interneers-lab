from . import core, use_cases, driven_ports, driving_ports
from random import randint

class CreateUserService(use_cases.CreateUserUseCase):

    def __init__(self, user_repositorty : driven_ports.UserRepositoryInterface):
        self.user_repositorty = user_repositorty

    def execute(self,user : driving_ports.CreateUser):
        user_exists = self.user_repositorty.find_by_email(user.email)

        if(user_exists):
            raise Exception("User already exists")
        else:
            new_user = core.User(user.name, user.email, randint(0,100000))
            self.user_repositorty.save(new_user)
            return new_user
