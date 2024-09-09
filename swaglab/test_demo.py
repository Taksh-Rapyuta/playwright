import re

import pytest
import asyncio
from playwright.async_api import async_playwright, expect,Page

async def test_shop():
    async with async_playwright() as p:
        browser= await p.chromium.launch(headless=False)
        context= await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page= await context.new_page()
        
        await page.goto("https://www.saucedemo.com/")
        await page.locator("[data-test=\"username\"]").fill("standard_user")
        await page.locator("[data-test=\"password\"]").fill("secret_sauce")
        await page.locator("[data-test=\"login-button\"]").click()
        await page.screenshot(path= "screenshots/login.png")
        await page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
        await page.screenshot(path= "screenshots/item.png")
        await page.goto("https://www.saucedemo.com/cart.html")
        await page.locator("#checkout").click()
        await page.screenshot(path= "screenshots/cart.png")
        await page.goto("https://www.saucedemo.com/checkout-step-one.html")
        await page.locator("[data-test=\"firstName\"]").fill("taksh")
        await page.locator("[data-test=\"lastName\"]").fill("prajapati")
        await page.locator("[data-test=\"postalCode\"]").fill("603203")
        await page.locator("#continue").click()
        await page.screenshot(path= "screenshots/address.png")
        await page.goto("https://www.saucedemo.com/checkout-step-two.html")
        await page.locator("#finish").click()
        await page.screenshot(path= "screenshots/finish.png")
        #stopping tracing
        await context.tracing.stop(path="logs/trace.zip")
        
        await browser.close()
        
asyncio.run(test_shop())

# def test_title(page: Page):
#     page.goto("https://www.saucedemo.com/")
#     page.locator("[data-test=\"username\"]").fill("standard_user")
#     page.locator("[data-test=\"password\"]").fill("secret_sauce")
#     page.locator("[data-test=\"login-button\"]").click()
#     page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
#     page.goto("https://www.saucedemo.com/cart.html")
#     page.locator("#checkout").click()
#     page.goto("https://www.saucedemo.com/checkout-step-one.html")
#     page.locator("[data-test=\"firstName\"]").fill("taksh")
#     page.locator("[data-test=\"lastName\"]").fill("prajapati")
#     page.locator("[data-test=\"postalCode\"]").fill("603203")
#     page.locator("#continue").click()
#     page.goto("https://www.saucedemo.com/checkout-step-two.html")
#     page.locator("#finish").click()
#         # assert page.title() == "Swag Labs"