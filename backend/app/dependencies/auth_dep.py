from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from backend.app.dependencies.repositories import user_repo
from backend.app.models.schemas import TokenPayload
from backend.app.models.user import User

from backend.core.config import settings
from backend.core.db import SessionDep
from backend.core.security import TokenDep


async def get_current_user(db: SessionDep, token: TokenDep) -> User:
    if not token:
        raise HTTPException(status_code=403, detail="Token not provided")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        raise HTTPException(status_code=403, detail="Invalid token")

    user = await user_repo.get_or_404(db=db, id=int(token_data.sub))
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
