import asyncio
from pyppeteer import launch


async def main():

	browser = await launch({ "headless": True, "args": ["--no-sandbox"] })
	url = await browser.newPage()
	await url.goto("https://scrapeme.live/shop/")
	await browser.close()




asyncio.get_event_loop().run_until_complete(main())
