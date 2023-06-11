import asyncio
from pyppeteer import launch


async def bot(name):

	url = "https://slither.io/"
	browser = await launch({ "headless": True,
							 "autoClose": True,
							 "args": [ "--start-maximized",
							 		   "--window-size=1920,1080" ] })

	page = await browser.newPage()
	await page.setViewport({ "width": 1920,
							 "height": 1080 })

	await page.goto(url)
	name_input = await page.querySelector("#nick")
	await name_input.type(name)
	await name_input.press("Enter")
	await asyncio.sleep(1)
	page = await pressKey(page, "ArrowLeft", 1)
	await asyncio.sleep(1)
	page = await checkReplay(page)
	page = await pressKey(page, "ArrowRight", 1)
	await asyncio.sleep(1)
	page = await checkReplay(page)
	page = await pressKey(page, "ArrowUp", 1)
	await asyncio.sleep(1)
	await browser.close()


async def pressKey(page, key, delay):

	await page.keyboard.down(key)
	await asyncio.sleep(delay)
	await page.keyboard.up(key)
	return page


async def checkReplay(page):

	xpath = "//div[contains(text(), 'Play')]"

	try:

		button = await page.xpath(xpath)

		if button:

			await button[0].click()

	except Exception as error:

		pass

	return page
