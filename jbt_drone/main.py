from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import config
from .resources import shutdown, startup
from .routers import drone, login

routers = [
    drone.router,
    login.router,
]

app = FastAPI(
    title='jbt_drone',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
)


for router in routers:
    app.include_router(router)


@app.on_event('startup')
async def startup_event() -> None:
    await startup()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await shutdown()
