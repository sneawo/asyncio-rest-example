from datetime import datetime
from typing import AsyncIterable, Dict
from aiohttp.web_exceptions import HTTPNotFound
from bson import ObjectId
from .models import Item


async def find_items() -> AsyncIterable[Item]:
    return Item.find({})


async def create_item(data: Dict) -> Item:
    item = Item(**data)
    await item.commit()
    return item


async def find_item(item_id: ObjectId) -> Item:
    item = await Item.find_one({'_id': item_id})
    if not item:
        raise HTTPNotFound()

    return item


async def update_item(item_id: ObjectId, data: Dict) -> Item:
    item = await find_item(item_id)

    item.update(data)
    item.updated_time = datetime.utcnow()
    await item.commit()

    return item


async def delete_item(item_id: ObjectId) -> None:
    item = await find_item(item_id)
    await item.delete()
