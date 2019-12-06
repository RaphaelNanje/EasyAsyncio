import asyncio
import datetime
import random

from easyasyncio import LoopManager, Consumer


class AutoSaveExample(Consumer):
    """print numbers asynchronously"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    async def fill_queue(self):
        for i in range(10000):
            if i not in self.context.data['numbers']:
                await self.queue.put(i)
        await self.queue_finished()

    async def work(self, number):
        """this logic gets called after an object is retrieved from the queue"""
        sum(list(range(number)))
        self.increment_stat()
        await asyncio.sleep(random.randint(1, 5))
        self.context.data['numbers'].add(number)

    async def tear_down(self):
        print(self.name, 'done at', datetime.datetime.now())

    @property
    def name(self):
        """
        Name the object or service being provided.
        This will effect how the StatsDisplay displays information about
        this Prosumer.
        """
        return 'consume_number'


manager = LoopManager()
consumer = AutoSaveExample(max_concurrent=15)

manager.context.data.register('numbers', set(), './numbers/numbers.txt')

manager.add_tasks(consumer)
manager.start()
