import asyncio
import logging
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo import MotorAsyncIOInstance


logger = logging.getLogger(__name__)
instance = MotorAsyncIOInstance()


async def init_mongo(app: web.Application, mongodb_uri: str) -> AsyncIOMotorDatabase:
    logger.info(f'init mongo')
    loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(mongodb_uri, io_loop=loop)
    return conn.get_database()


async def setup_mongo(app: web.Application) -> None:
    config = app['config']
    app['db'] = await init_mongo(app, config.MONGODB_URI)
    instance.init(app['db'])

    async def close_mongo(app: web.Application) -> None:
        logger.info('close mongo')
        app['db'].client.close()

    app.on_cleanup.append(close_mongo)
