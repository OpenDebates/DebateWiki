from typing import Any, Dict, Union

from fastapi import APIRouter, Depends, Request, Response
from fastapi_users import FastAPIUsers, InvalidPasswordException
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase

from loguru import logger
from DebateWiki import config
from DebateWiki.models import User, UserCreate, UserDB, UserModel, UserUpdate

router = APIRouter(prefix="/api/v1")


# Instantiate User DB
user_db = TortoiseUserDatabase(UserDB, UserModel)
jwt_authentication = JWTAuthentication(
    secret=config["api"]["jwt_secret"], lifetime_seconds=3600, name="jwt-v1"
)


async def validate_password(password: str, user: Union[UserCreate, User]) -> None:
    if len(password) < 8:
        raise InvalidPasswordException(
            reason="Password should be at least 8 characters"
        )
    if user.email in password:
        raise InvalidPasswordException(reason="Password should not contain e-mail")


fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
    validate_password=validate_password,
)


@router.post("/auth/jwt/refresh", tags=["Authentication"])
async def refresh_jwt(
    response: Response, user=Depends(fastapi_users.get_current_active_user)
):
    return await jwt_authentication.get_login_response(user, response)


def on_after_register(user: UserDB, request: Request):
    logger.info(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    logger.info(f"User {user.id} has forgot their password. Reset token: {token}")


def on_after_reset_password(user: UserDB, request: Request):
    logger.info(f"User {user.id} has reset their password.")


def on_after_update(user: UserDB, updated_user_data: Dict[str, Any], request: Request):
    logger.info(
        f"User {user.id} has been updated with the following data: {updated_user_data}"
    )


def after_verification_request(user: UserDB, token: str, request: Request):
    logger.info(f"Verification requested for user {user.id}. Verification token: {token}")


router.include_router(
    fastapi_users.get_auth_router(jwt_authentication, requires_verification=True),
    prefix="/auth/jwt",
    tags=["Authentication"],
)
router.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["Authentication"],
)
router.include_router(
    fastapi_users.get_reset_password_router(
        config["api"]["reset_secret"],
        after_forgot_password=on_after_forgot_password,
        after_reset_password=on_after_reset_password,
    ),
    prefix="/auth",
    tags=["Authentication"],
)

router.include_router(
    fastapi_users.get_verify_router(
        config["api"]["verify_secret"],
        after_verification_request=after_verification_request,
    ),
    prefix="/auth",
    tags=["Authentication"],
)

router.include_router(
    fastapi_users.get_users_router(on_after_update, requires_verification=True),
    prefix="/users",
    tags=["Users"],
)
