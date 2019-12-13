import asyncio

from easyasyncio import Producer, LoopManager, Consumer
from easyasyncio.stats import StatsDisplay


class CharConsumer(Consumer):
    """print numbers asynchronously"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def work(self, char):
        """this logic gets called after an object is retrieved from the queue"""
        await asyncio.sleep(1, 5)
        self.logger.info(char)
        self.increment_stat()

    @property
    def name(self):
        """
        Name the object or service being provided.
        This will effect how the StatsDisplay displays information about
        this Prosumer.
        """
        return 'consume_char'


class CharProducer(Producer):

    def __init__(self, data: str, **kwargs):
        super().__init__(list(data), **kwargs)

    async def fill_queue(self):
        for i in self.input_data:
            await self.queue.put(i)

    async def work(self, char):
        self.logger.debug('%s adding %s to consume_number queue', self.name, char)
        await self.context.queues['consume_char'].put(char)
        self.increment_stat()

    async def tear_down(self):
        await self.successor.queue_finished()

    @property
    def name(self):
        return 'produce_char'


manager = LoopManager()
producer = CharProducer('Hello Worldddddddddddddddddddddddddddddddddddddddddddddddddd', max_concurrent=5)
consumer = CharConsumer()
producer.add_successor(consumer)
# producer.add_successor(consumer)
manager.add_tasks(producer, consumer)
data_thread = StatsDisplay(manager.context)
manager.run()
