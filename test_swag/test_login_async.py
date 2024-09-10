
import pytest
from playwright.async_api import async_playwright

@pytest.fixture(scope="function")
async def browser_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        yield context
        await context.close()
        await browser.close()

@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])       
async def test_successful_login(browser_context, username):
    page = await browser_context.new_page()
    await page.goto("https://www.saucedemo.com/")
    await page.get_by_placeholder('Username').fill(username)
    await page.get_by_placeholder('Password').fill('secret_sauce')
    await page.get_by_role('button', name='Login').click()
    
    if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user", "error_user"]:
        
        inventory_container = page.locator('[data-test="inventory-container"]')
        assert await inventory_container.is_visible()
    else:
        if username == "locked_out_user":
            error_message_locator = page.locator('[data-test="error"]')
            assert await error_message_locator.is_visible()

@pytest.mark.parametrize("username, password", [
    ("invalid_user", "wrong_password"),
])
async def test_invalid_login(browser_context, username, password):
    page = await browser_context.new_page()
    await page.goto("https://www.saucedemo.com/")
    await page.get_by_placeholder('Username').fill(username)
    await page.get_by_placeholder('Password').fill(password)
    await page.get_by_role('button', name='Login').click()
    
    # Check for the presence of the error message
    error_message_element = page.locator('[data-test="error"]')
    assert await error_message_element.is_visible()

@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])            
async def test_unsuccessful_login_username_credentials(browser_context, username):
    page = await browser_context.new_page()
    await page.goto("https://www.saucedemo.com/")
    await page.get_by_placeholder('Username').fill(username)
    await page.get_by_placeholder('Password').fill("")
    await page.get_by_role('button', name='Login').click()
    error_message_element = page.locator('[data-test="error"]')
    assert await error_message_element.is_visible()     

async def test_unsuccessful_login_password_credentials(browser_context):
    page = await browser_context.new_page()
    await page.goto("https://www.saucedemo.com/")
    await page.get_by_placeholder('Username').fill("")
    await page.get_by_placeholder('Password').fill("secret_sauce")
    await page.get_by_role('button', name='Login').click()
    error_message_element = page.locator('[data-test="error"]')
    assert await error_message_element.is_visible() 

async def test_unsuccessful_login_empty_credentials(browser_context):
    page = await browser_context.new_page()
    await page.goto("https://www.saucedemo.com/")
    await page.get_by_placeholder('Username').fill("")
    await page.get_by_placeholder('Password').fill("")
    await page.get_by_role('button', name='Login').click()
    error_message_element =page.locator('[data-test="error"]')
    assert await error_message_element.is_visible()
