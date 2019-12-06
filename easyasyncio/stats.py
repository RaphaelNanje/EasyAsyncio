import asyncio
import time
from collections import Counter
from typing import TYPE_CHECKING

from . import logger

if TYPE_CHECKING:
    from .context import Context


class Stats(Counter):
    """keep track of various stats"""
    start_time = time.time()
    _end_time = None
    data_found = 0
    initial_data_count = 0

    def __init__(self, context) -> None:
        from .context import Context
        self.context: Context = context
        super().__init__()

    @property
    def end_time(self):
        return self._end_time or time.time()

    def get_count_strings(self):
        string = '\n'
        string += '\t\t\t    <-----STATS----->'
        string += '\n\t\t\t    elapsed time: {time:.6f} secs\n'.format(time=self.elapsed_time)
        if self.items():
            for k, v in self.items():
                string += f'\t\t\t    {k} count: {v}\n'
                string += f'\t\t\t    {k}\'s count per second: {v / self.elapsed_time}\n'
        string += '\t\t\t    </-----STATS----->\n\n'
        for p in self.context.workers:
            from .consumer import Consumer
            top_worker_section_string = f'<-----WORKER {p.name}----->\n'
            string += '\t\t\t    ' + top_worker_section_string
            if isinstance(p, Consumer):
                string += f'\t\t\t    {p.name} queue: {p.working + p.queue.qsize()} items left\n'
            else:
                string += f'\t\t\t    {p.name} queue: {p.queue.qsize()} items left\n'
            string += f'\t\t\t    {p.name} workers: {p.max_concurrent}\n'
            string += f'\t\t\t    {p.name} status: {p._status}\n'
            i = 1 if len(top_worker_section_string) % 2 != 0 else 4
            string += (f'\t\t\t    </'
                       f'{"-" * int((len(top_worker_section_string) / 3 - i))}'
                       f'WORKER'
                       f'{"-" * int((len(top_worker_section_string) / 3))}----->\n\n')
        return string.rstrip()

    def get_stats_string(self):
        string = '\n\t\t    <---------------------SESSION STATS--------------------->'
        string += self.get_count_strings()
        string += '\n\t\t    </---------------------SESSION STATS--------------------->\n'

        return string

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time


class StatsDisplay:
    name = 'StatsDisplay'
    interval = 15

    def __init__(self, context: 'Context') -> None:
        super().__init__()
        self.context = context
        if self.context.stats_thread:
            del self.context.stats_thread
        self.context.stats_thread = self

    async def run(self) -> None:
        logger.debug('%s starting...', self.name)
        while self.context.running:
            logger.debug('%s\n', self.context.stats.get_stats_string() + self.context.data.get_data_string())
            await asyncio.sleep(self.interval)
            if not self.context.running:
                break
