from fastapi import FastAPI
from fastapi import Request
from starlette.responses import JSONResponse

from app.errors import AppException
from app.routers.analytics_router import router as analytics_router
from app.routers.order_router import router as order_router
from app.routers.product_router import router as product_router
from app.routers.category_router import router as category_router
from app.routers.auth_yandex_router import router as auth_yandex_router
from app.routers.auth_router import router as auth_router
from app.routers.cart_router import router as cart_router


app = FastAPI(title="Furs & Fur Coats API")

@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.code,
        content=exc.to_dict()
    )

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(auth_router)
app.include_router(auth_yandex_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(analytics_router)

@app.get("/health")
def health():
    return {"status": "ok"}




