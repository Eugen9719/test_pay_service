from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from backend.app.dependencies.auth_dep import CurrentUser
from backend.app.dependencies.services import registration_service, user_auth, user_service
from backend.app.models.schemas import Token, Msg
from backend.app.models.user import UserRead, UserCreate, UserAccountRead, UserUpdate

from backend.core import security
from backend.core.config import settings

from backend.core.db import TransactionSessionDep, SessionDep

user_router = APIRouter()


@user_router.post("/login/access-token", response_model=Token)
async def login_access_token(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await user_auth.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            str(user.id), expires_delta=access_token_expires
        ), token_type="bearer"
    )


@user_router.post("/registration", response_model=UserRead)
async def user_create(schema: UserCreate, db: TransactionSessionDep, current_user: CurrentUser):
    return await registration_service.create_user(db=db, schema=schema, current_user=current_user)


@user_router.get('/me', response_model=UserAccountRead)
async def get_user_me(db:SessionDep, current_user: CurrentUser):
    return await user_service.get_user_me(db=db, current_user=current_user)


@user_router.patch("/update_user/{user_id}", response_model=UserRead)
async def update_user(*, db: TransactionSessionDep, user_id: int, schema: UserUpdate, current_user: CurrentUser):
    return await user_service.update_user(db=db, user_id=user_id, schema=schema, current_user=current_user)


@user_router.delete("/delete/{user_id}", response_model=Msg)
async def delete_user(user_id: int, db: TransactionSessionDep, current_user: CurrentUser):
    return await user_service.delete_user(db=db, current_user=current_user, user_id=user_id)


@user_router.get("/all_user", response_model=List[UserAccountRead])
async def get_all_user(db: SessionDep, current_user: CurrentUser):
    return await user_service.get_users(db=db, current_user=current_user)
