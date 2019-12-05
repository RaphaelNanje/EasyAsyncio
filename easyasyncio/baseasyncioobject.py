from abc import abstractmethod
from asyncio import AbstractEventLoop, Semaphore, Future
from typing import Set

from . import logger
from .context import Context


# noinspection PyMethodMayBeStatic
class BaseAsyncioObject:
    tasks: Set[Future]
    max_concurrent: int
    context: Context
    logger = logger
    loop: AbstractEventLoop
    sem: Semaphore
    successor: 'BaseAsyncioObject' = None
    _done = False
    results = []

    def __init__(self, max_concurrent=10) -> None:
        self.tasks = set()
        self.max_concurrent = max_concurrent

    @property
    def queue(self):
        return self.context.queues.get(self.name)

    def increment_stat(self, n=1):
        """increment the count of whatever this prosumer is processing"""
        self.context.stats[self.name] += n

    def initialize(self, context: Context):
        self.context = context
        self.loop = context.loop
        self.context.workers.add(self)
        self.sem = Semaphore(self.max_concurrent)
        self.context.queues.new(self.name)
        self.status('initialized')

    async def preprocess(self, item):
        """do any pre-processing to the queue item here"""
        return item

    async def postprocess(self, item):
        """do any postprocessing to the resulting item here"""
        return item

    async def queue_finished(self):
        """called when all tasks are finished with queue"""
        self.logger.debug(self.name + ' finished queueing')
        await self.queue.put(False)

    async def fill_queue(self):
        pass

    def status(self, *strings: str):
        self.context.data[f'{self.name}\'s status'] = ' '.join(
            [str(s) if not isinstance(s, str) else s for s in strings])

    async def tear_down(self):
        """this is called after all tasks are completed"""
        pass

    async def queue_successor(self, data):
        await self.successor.queue.put(data)

    def add_successor(self, successor: 'BaseAsyncioObject'):
        """
        The next async worker that will work on the data that this async worker gathers
        """
        assert successor != self
        self.successor = successor

    @abstractmethod
    async def run(self):
        """setup workers and start"""
        pass

    @abstractmethod
    async def work(self, *args):
        """do business logic on each enqueued item"""
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
