from bson import ObjectId
from aiohttp.test_utils import unittest_run_loop
from app.models import Item
from tests import AppTestCase


class ItemListTestCase(AppTestCase):

    @unittest_run_loop
    async def test_list(self):
        item1 = Item(name='item1')
        await item1.commit()
        item2 = Item(name='item2')
        await item2.commit()

        resp = await self.client.get("/items")
        assert resp.status == 200
        items = await resp.json()
        assert len(items) == 2


class ItemCreateTestCase(AppTestCase):

    @unittest_run_loop
    async def test_create_item(self):
        data = {
            'name': 'item1'
        }
        resp = await self.client.post("/items", json=data)
        assert resp.status == 201

        item = await Item.find_one({})
        assert item.name == data['name']

    @unittest_run_loop
    async def test_bad_request(self):
        data = {
            'bad_key': 'item1'
        }
        resp = await self.client.post(f"/items", json=data)
        assert resp.status == 400


class ItemUpdateTestCase(AppTestCase):

    @unittest_run_loop
    async def test_update(self):
        item = Item(name='test')
        await item.commit()
        data = {
            'name': 'item1'
        }
        resp = await self.client.put(f"/items/{item.id}", json=data)
        assert resp.status == 200

        await item.reload()
        assert item.name == data['name']
        assert item.updated_time

    @unittest_run_loop
    async def test_not_found(self):
        data = {
            'name': 'item1'
        }
        resp = await self.client.put(f"/items/{ObjectId()}", json=data)
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.put(f"/items/{'x'*24}", json={})
        assert resp.status == 400

    @unittest_run_loop
    async def test_bad_request(self):
        item = Item(name='test')
        await item.commit()
        data = {
            'bad_key': 'item1'
        }
        resp = await self.client.put(f"/items/{item.id}", json=data)
        assert resp.status == 400


class ItemDeleteTestCase(AppTestCase):

    @unittest_run_loop
    async def test_delete(self):
        item = Item(name='item1')
        await item.commit()
        resp = await self.client.delete(f"/items/{item.id}")
        assert resp.status == 204

        assert not (await Item.find_one({'_id': item.id}))

    @unittest_run_loop
    async def test_not_found(self):
        resp = await self.client.delete(f"/items/{ObjectId()}")
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.delete(f"/items/{'x'*24}")
        assert resp.status == 400


class ItemGetTestCase(AppTestCase):

    @unittest_run_loop
    async def test_get(self):
        item = Item(name='item1')
        await item.commit()
        resp = await self.client.get(f"/items/{item.id}")
        assert resp.status == 200
        data = await resp.json()
        assert data['id'] == str(item.id)
        assert data['name'] == item.name

    @unittest_run_loop
    async def test_not_found(self):
        resp = await self.client.get(f"/items/{ObjectId()}")
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.get(f"/items/{'x'*24}")
        assert resp.status == 400
