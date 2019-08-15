from aiohttp.test_utils import AioHTTPTestCase
from app.main import init
from app.config import TestConfig


class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return init(TestConfig())

    async def tearDownAsync(self) -> None:
        await self.app['db'].client.drop_database(self.app['db'])
