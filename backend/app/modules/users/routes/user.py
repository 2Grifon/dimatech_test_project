from fastapi import APIRouter

from app.core.dependencies import CurrentUserDep
from app.modules.users.schemas import UserRead
from app.modules.users.services.user import UserServiceDep

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
async def get_me(
    current_user: CurrentUserDep,
) -> UserRead:
    return current_user


@router.get("/me/accounts")
async def get_my_accounts(service: UserServiceDep, current_user: CurrentUserDep):
    return await service.get_accounts(current_user)


@router.get("/me/payments")
async def get_my_payments(service: UserServiceDep, current_user: CurrentUserDep):
    return await service.get_payments(current_user)
