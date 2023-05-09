import uuid
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend

from auth.manager import get_user_manager
from auth.models import User

app = FastAPI()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
