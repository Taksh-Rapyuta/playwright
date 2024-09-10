import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])       
def test_successful_login(browser_context,username):
    page= browser_context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder('Username').fill(username)
    page.get_by_placeholder('Password').fill('secret_sauce')
    page.get_by_role('button', name='Login').click()
    if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user,error_user"]:
        assert page.locator("[data-test='inventory-container']").is_visible()
    else:
        if username == "locked_out_user":
            error_message_element = page.get_by_text("Epic sadface:")
            assert error_message_element.is_visible()
            
@pytest.mark.parametrize("username, password", [
    ("invalid_user", "wrong_password"),
])
def test_invalid_login(browser_context, username, password):
    page = browser_context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder('Username').fill(username)
    page.get_by_placeholder('Password').fill(password)
    page.get_by_role('button', name='Login').click()
    
    # Check for the presence of the error message
    error_message_element = page.get_by_text("Epic sadface:")
    assert error_message_element.is_visible()
@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])            
def test_unsuccessful_login_username_credentials(browser_context,username):
    page = browser_context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder('Username').fill(username)
    page.get_by_placeholder('Password').fill("")
    page.get_by_role('button', name='Login').click()
    error_message_element = page.get_by_text("Epic sadface:")
    assert error_message_element.is_visible()     
    
def test_unsuccessful_login_password_credentials(browser_context):
    page = browser_context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder('Username').fill("")
    page.get_by_placeholder('Password').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()
    error_message_element = page.get_by_text("Epic sadface:")
    assert error_message_element.is_visible() 
    
def test_unsuccessful_login_empty_credentials(browser_context):
    page = browser_context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder('Username').fill("")
    page.get_by_placeholder('Password').fill("")
    page.get_by_role('button', name='Login').click()
    error_message_element = page.get_by_text("Epic sadface:")
    assert error_message_element.is_visible()    
