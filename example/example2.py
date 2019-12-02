import asyncio

from easyasyncio import Producer, LoopManager, Constants


class WithSessionProducer(Producer):
    """requests websites asynchronously"""

    def __init__(self, data: int):
        super().__init__(data)

    async def fill_queue(self):
        """override this abstract class to fill the queue"""
        for i in range(0, self.data):
            await self.queue.put(i)

    async def work(self, number):
        """implement the business logic here"""
        await asyncio.sleep(1)
        async with self.context.session.get(
                'http://127.0.0.1:5500/temp.html',
                headers=Constants.HEADERS
        ) as response:
            text = await response.read()
            self.logger.info(text)
        self.append()

    @property
    def name(self):
        """
        Name the object or service being provided.
        This will effect how the DataHandler displays information about
        this Prosumer.
        """
        return 'parse_request'


manager = LoopManager()
manager.add_tasks(WithSessionProducer(10))

manager.start(use_session=True)
