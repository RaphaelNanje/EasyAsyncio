import abc
import asyncio
from abc import abstractmethod

from .baseasyncioobject import BaseAsyncioObject


class Producer(BaseAsyncioObject, metaclass=abc.ABCMeta):
    start = False  # whether this Producer will start instantly or not

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    @abstractmethod
    async def fill_queue(self):
        """implement the queue filling logic here"""
        pass

    async def worker(self, num):
        """get each item from the queue and pass it to self.work"""
        self.logger.debug('%s worker %s started', self.name, num)
        while self.context.running:
            data = await self.queue.get()
            if data is False:
                self.logger.debug('%s worker %s terminating', self.name, num)
                break
            # self.logger.debug('%s worker %s retrieved queued data %s', self.name, num, data)
            data = await self.preprocess(data)
            async with self.sem:
                result = await self.work(data)
                self.queue.task_done()
                self.results.append(await self.postprocess(result))

    async def run(self):
        try:
            self.status('populating queue')
            await self.fill_queue()
            self.logger.debug(self.name + ' finished populating queue')
        except Exception as e:
            self.logger.exception(e)
            raise e
        else:
            self.logger.info('%s starting...', self.name)
            self.status('creating workers')
            for _ in range(self.max_concurrent):
                self.logger.debug(self.name + ' creating workers')
                self.tasks.add(self.loop.create_task(self.worker(_)))

            self.logger.debug(self.name + ' finished creating workers')
            self.status('awaiting tasks to finish')
            await self.queue_finished()
            await asyncio.gather(*self.tasks)
            await self.tear_down()
            self.status('finished')
            self.logger.info('%s is finished: %s', self.name, self.results)
