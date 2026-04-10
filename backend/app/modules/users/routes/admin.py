from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies import CurrentAdminDep

from app.modules.accounting.schemas.account import AccountRead
from app.modules.users.schemas.user import UserRead, UserCreate, UserUpdate
from app.modules.users.services.admin import AdminServiceDep

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def get_users(
    service: AdminServiceDep,
    _: CurrentAdminDep,
) -> list[UserRead]:
    return await service.get_users()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: AdminServiceDep,
    _: CurrentAdminDep,
) -> UserRead:
    return await service.create_user(data)


@router.patch("/users/{user_id}")
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: AdminServiceDep,
    _: CurrentAdminDep,
) -> UserRead:
    return await service.update_user(user_id, data)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: AdminServiceDep,
    _: CurrentAdminDep,
) -> None:
    await service.delete_user(user_id)


@router.get("/users/{user_id}/accounts")
async def get_user_accounts(
    user_id: UUID,
    service: AdminServiceDep,
    _: CurrentAdminDep,
) -> list[AccountRead]:
    return await service.get_user_accounts(user_id)
