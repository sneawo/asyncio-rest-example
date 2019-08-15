import logging
from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest
from bson import ObjectId
from bson.objectid import InvalidId
from umongo import ValidationError
from . import services, schemas

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)


def validate_object_id(object_id: str) -> ObjectId:
    try:
        object_id = ObjectId(object_id)
    except InvalidId:
        logger.error(f'invalid id {object_id}')
        raise HTTPBadRequest(reason='Invalid id.')
    return object_id


@routes.get('/items')
async def list_items(request: web.Request) -> web.Response:
    items = await services.find_items()
    return web.json_response([item.dump() async for item in items], status=200)


@routes.post('/items')
async def create_item(request: web.Request) -> web.Response:
    try:
        schema = schemas.ItemSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)

    item = await services.create_item(data)
    return web.json_response(item.dump(), status=201)


@routes.get(r'/items/{item_id:\w{24}}')
async def get_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])
    item = await services.find_item(item_id)

    return web.json_response(item.dump(), status=200)


@routes.put(r'/items/{item_id:\w{24}}')
async def update_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])

    try:
        schema = schemas.UpdateItemSchema(strict=True)
        data = schema.load(await request.json()).data
    except ValidationError as error:
        logger.error('validation error', extra={'errors': error.messages})
        raise HTTPBadRequest(reason=error.messages)

    item = await services.update_item(item_id, data)

    return web.json_response(item.dump(), status=200)


@routes.delete(r'/items/{item_id:\w{24}}')
async def delete_item(request: web.Request) -> web.Response:
    item_id = validate_object_id(request.match_info['item_id'])
    await services.delete_item(item_id)

    return web.json_response({}, status=204)
