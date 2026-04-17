# FastScrapy

Lightweight async web scraper framework for concurrent scraping.

## Why fastscrapy?

1. **Worker inheritance**: Override `worker()` to define your scraping logic
1. **Pure async**: Built on asyncio and aiohttp. No callbacks, no frameworks
1. **Minimal**: ~50 lines of code. Learn it in 5 minutes

## Quick Start

```python
from fastscrapy import FastScraper

class MyScraper(FastScraper):

	def __init__(self, num_pages: int):
		self.remaining_pages = set(range(num_pages))
		self.url = 'https://jsonplaceholder.typicode.com/posts'

	# override this function
	async def worker(self, worker_id: int):
		while self.remaining_pages:
			page = self.remaining_pages.pop()

			response = await self.request(self.url, params={
				'_page': page,
				'_limit': 10
			})

			posts = await response.json()
			print(f"Worker {worker_id}: page {page} has {len(posts)} posts")


scraper = MyScraper(100)

# invoke 5 worker functions asynchronously
scraper.run(num_workers=5)

```
