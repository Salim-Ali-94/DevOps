import asyncio
from pyppeteer import launch


async def bot():

	url = "https://slither.io/"
	browser = await launch({ "headless": False,
							 "autoClose": False,
							 "args": [ "--start-maximized",
							 		   "--window-size=1920,1080" ] })

	page = await browser.newPage()
	await page.setViewport({ "width": 1920, 
							 "height": 1080 })

	await page.goto(url)
	name_input = await page.querySelector("#nick")
	await name_input.type("snake_name")
	await name_input.press("Enter")
	await asyncio.sleep(2)
	await page.keyboard.down("ArrowLeft")
	await asyncio.sleep(2)
	await page.keyboard.up("ArrowLeft")
	await asyncio.sleep(1)
	await page.keyboard.down("ArrowRight")
	await asyncio.sleep(2)
	await page.keyboard.up("ArrowRight")
	await asyncio.sleep(1)
	await page.keyboard.down("ArrowUp")
	await asyncio.sleep(5)
	await page.keyboard.up("ArrowUp")
	await asyncio.sleep(1)




if __name__ == "__main__":

	asyncio.run(bot())
