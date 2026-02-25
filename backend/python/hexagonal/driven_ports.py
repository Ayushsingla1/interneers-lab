from . import core
from abc import ABC, abstractmethod

class UserRepositoryInterface(ABC):

    @abstractmethod
    def save(self,user :core.User):
        pass

    @abstractmethod
    def find_by_email(self,email : str):
        pass