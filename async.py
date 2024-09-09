import asyncio 
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser=await p.firefox.launch(headless=False)
        page=await browser.new_page()
        await page.goto("https://www.lambdatest.com/learning-hub/pytest-api-testing")
        print(await page.title())
        browser.close()
        
asyncio.run(main())