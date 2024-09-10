import pytest
import asyncio
import re
from playwright.async_api import async_playwright, expect,Page

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.saucedemo.com/")
        
        # Test 1: Login with valid credentials
        await page.locator("[data-test='username']").fill("standard_user")
        await page.locator("[data-test='password']").fill("secret_sauce")
        await page.locator("[data-test='login-button']").click()

        # Expect successful login to inventory page
        await expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        await page.screenshot(path="screenshots/login_success.png")

        # Test 2: Login with missing username
        await page.goto("https://www.saucedemo.com/")
        await page.locator("[data-test='password']").fill("secret_sauce")
        await page.locator("[data-test='login-button']").click()

        # Expect error for missing username
        error_msg = page.locator("[data-test='error']")
        await expect(error_msg).to_have_text("Epic sadface: Username is required")
        await page.screenshot(path="screenshots/missing_username.png")

        # Test 3: Login with missing password
        await page.goto("https://www.saucedemo.com/")
        await page.locator("[data-test='username']").fill("standard_user")
        await page.locator("[data-test='login-button']").click()

        # Expect error for missing password
        await expect(error_msg).to_have_text("Epic sadface: Password is required")
        await page.screenshot(path="screenshots/missing_password.png")

        # Test 4: Login with wrong credentials
        await page.goto("https://www.saucedemo.com/")
        await page.locator("[data-test='username']").fill("standard_user")
        await page.locator("[data-test='password']").fill("wrong_password")
        await page.locator("[data-test='login-button']").click()

        # Expect error for invalid login
        await expect(error_msg).to_have_text("Epic sadface: Username and password do not match any user in this service")
        await page.screenshot(path="screenshots/wrong_credentials.png")
        
        
# Run the test function
asyncio.run(test_login())