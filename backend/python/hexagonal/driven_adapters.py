from . import core, driven_ports

class InMemoryUserRepository(driven_ports.UserRepositoryInterface):

    def __init__(self):
        self.users : list[core.User] = []

    def find_by_email(self,email : str): 
        for user in self.users:
            if(user.email == email):
                return True
    
        return False
    
    def save(self,user : core.User):
        self.users.append(user)