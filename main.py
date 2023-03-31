from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import routers.analytics
import routers.preprocess
import routers.annotations
import routers.repair
import routers.merging
import routers.loading
import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sinatra API",
        version="1.0",
        description="Sinatra API docs and schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

BASE_URI = f"/api/v{settings.API_VERSION}"


app.include_router(routers.loading.router, prefix=BASE_URI)
app.include_router(routers.analytics.router, prefix=BASE_URI)
app.include_router(routers.preprocess.router, prefix=BASE_URI)
app.include_router(routers.annotations.router, prefix=BASE_URI)
app.include_router(routers.repair.router, prefix=BASE_URI)
app.include_router(routers.merging.router, prefix=BASE_URI)




