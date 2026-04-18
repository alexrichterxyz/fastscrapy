import asyncio
import aiohttp
from abc import ABC, abstractmethod

class FastScraper(ABC):
	timeout: int = 10

	@property
	def client_timeout(self):
		return aiohttp.ClientTimeout(total=self.timeout)

	async def request(self, url: str, method: str = 'GET', **kwargs):
		"""Make HTTP request."""
		return await self.session.request(method, url, timeout=self.client_timeout, **kwargs)

	@abstractmethod
	async def worker(self, worker_id: int):
		"""Override to define worker logic."""
		pass

	async def _run_async(self, num_workers: int):
		"""Run workers concurrently."""
		async with aiohttp.ClientSession(timeout=self.client_timeout) as session:
			self.session = session
			await asyncio.gather(*[
				self.worker(i) for i in range(num_workers)
			])

	def run(self, num_workers: int):
		"""Run workers concurrently. Sync entry point."""
		asyncio.run(self._run_async(num_workers))