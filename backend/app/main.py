from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.modules.users.routes import auth_router, user_router, admin_router
from app.modules.accounting.routes import webhook_router

from app.modules.accounting import models as accounting_models  # NOQA F401
from app.modules.users import models as users_models  # NOQA F401

app = FastAPI(title="Dimatech test project API", prefix=settings.API_PREFIX)

main_router = APIRouter(prefix=settings.API_PREFIX)

main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(admin_router)
main_router.include_router(webhook_router)

app.include_router(main_router)
