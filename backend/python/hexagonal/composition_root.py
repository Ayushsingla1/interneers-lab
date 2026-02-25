from . import driven_adapters, driving_adapters, service

im_memory_repository = driven_adapters.InMemoryUserRepository()
user_service = service.CreateUserService(im_memory_repository)
user_controller = driving_adapters.UserController(user_service)

