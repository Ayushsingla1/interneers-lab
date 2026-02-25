from abc import ABC, abstractmethod

class CreateUser:

    def __init__(self, name, email):
        self.name = name
        self.email = email

class CreateUserUseCase(ABC):

    @abstractmethod
    def execute(self,user : CreateUser):
        pass