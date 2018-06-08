import logging
import aiohttp_cors
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from .routes import setup_routes
from .settings import config


async def init_db_client(app) -> None:
    """ Initialize async MongoDB client and store db and collection in app"""
    mongo_conf = app['config']['mongo']
    app['db'] = AsyncIOMotorClient(mongo_conf['host'], mongo_conf['port'])[mongo_conf['database']]
    app['collection'] = app['db'][mongo_conf['collection']]


# set logging level
logging.basicConfig(level=logging.INFO)
app = web.Application()
app['config'] = config
setup_routes(app)
# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "http://localhost:3000": aiohttp_cors.ResourceOptions(
        allow_headers=("Access-Control-Allow-Origin",)
    )
})
# !!! Allow cors for all routes !!!
for route in list(app.router.routes()):
    cors.add(route)
app.on_startup.append(init_db_client)
web.run_app(app, port=config['port'])
