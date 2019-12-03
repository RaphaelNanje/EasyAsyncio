from abc import abstractmethod
from asyncio import AbstractEventLoop, Semaphore, Task
from typing import Set

from easyasyncio import logger
from .context import Context


class BaseAsyncioObject:
    tasks: Set[Task]
    max_concurrent = 5
    context: Context
    logger = logger
    loop: AbstractEventLoop
    sem: Semaphore
    successor: 'BaseAsyncioObject' = None
    _done = False
    results = []

    def __init__(self) -> None:
        super().__init__()
        self.tasks = set()

    @property
    def queue(self):
        return self.context.queues.get(self.name)

    def increment_stat(self, n=1):
        """increment the count of whatever this prosumer is processing"""
        self.context.stats[self] += n

    def initialize(self, context: Context):
        self.context = context
        self.loop = context.loop
        self.context.workers.add(self)
        self.sem = Semaphore(self.max_concurrent)

    async def preprocess(self, item):
        """do any pre-processing to the queue item here"""
        return item

    async def postprocess(self, item):
        """do any postprocessing to the resulting item here"""
        return item

    async def queue_finished(self):
        """called when all tasks are finished with queue"""
        self.logger.debug(self.name + ' calling queue_finished()')
        for _ in self.tasks:
            await self.queue.put(False)

    async def fill_queue(self):
        pass

    async def tear_down(self):
        """this is called after all tasks are completed"""
        pass

    async def finished(self):
        """called after tear_down"""
        if self.successor:
            self.context.loop_manager.add_tasks(self.successor)

    def add_successor(self, successor: 'BaseAsyncioObject'):
        """
        The next async worker that will start after this task completes.
        WARNING: The method will cause a dirty shutdown
        """
        # todo complete this logic
        self.successor = successor
        import warnings
        warnings.warn(RuntimeWarning('The method will cause a dirty shutdown'), stacklevel=2)

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
