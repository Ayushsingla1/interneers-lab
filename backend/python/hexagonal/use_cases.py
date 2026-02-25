from . import driving_ports
from abc import ABC, abstractmethod

class CreateUserUseCase(ABC):

    @abstractmethod
    def execute(self,user : driving_ports.CreateUser):
        pass