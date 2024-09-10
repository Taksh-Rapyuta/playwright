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
def test_add_single_item_to_cart(browser_context,username):
        page = browser_context.new_page()

        # Navigate to the site
        page.goto("https://www.saucedemo.com/")

        page.goto("https://www.saucedemo.com/")
        page.get_by_placeholder('Username').fill(username)
        page.get_by_placeholder('Password').fill('secret_sauce')
        page.get_by_role('button', name='Login').click()
        if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user,error_user"]:
            assert page.locator("[data-test='inventory-container']").is_visible()
            
            
            page.locator("[data-test=\"inventory-list\"] div").filter(has_text="Sauce Labs Backpack").nth(1).click()
            page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()

        
            cart_count = page.inner_text('.shopping_cart_badge')
            assert cart_count == "1"
        else:
            if username == "locked_out_user":
                error_message_element = page.get_by_text("Epic sadface:")
                assert error_message_element.is_visible()

@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    # "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])

def test_add_multiple_items_to_cart(browser_context,username):
        page = browser_context.new_page()

        # Navigate to the site
        page.goto("https://www.saucedemo.com/")

        page.get_by_placeholder('Username').fill(username)
        page.get_by_placeholder('Password').fill('secret_sauce')
        page.get_by_role('button', name='Login').click()
        if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user,error_user"]:
            assert page.locator("[data-test='inventory-container']").is_visible()

            # Add multiple items to the cart
            
            page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
            page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()
            page.locator("[data-test=\"add-to-cart-sauce-labs-bolt-t-shirt\"]").click()
            page.locator("[data-test=\"add-to-cart-sauce-labs-fleece-jacket\"]").click()

            # Check the cart count
            cart_count = page.inner_text('.shopping_cart_badge')
            assert cart_count == "4"  # Adjust this if you add/remove items dynamically
        
        else:
            if username == "locked_out_user":
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
def test_remove_item_from_cart(browser_context,username):
    
        page = browser_context.new_page()

        # Navigate to the site
        page.goto("https://www.saucedemo.com/")

        page.get_by_placeholder('Username').fill(username)
        page.get_by_placeholder('Password').fill('secret_sauce')
        page.get_by_role('button', name='Login').click()
        if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user,error_user"]:
            assert page.locator("[data-test='inventory-container']").is_visible()

            # Add an item to the cart
            page.locator("[data-test=\"inventory-list\"] div").filter(has_text="Sauce Labs Backpack").nth(1).click()
            page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()

            # Go to the cart
            page.click('.shopping_cart_link')

            # Remove the item from the cart
            page.locator("[data-test=\"remove-sauce-labs-backpack\"]").click()

            # Verify that the cart is empty
            cart_count = page.query_selector('.shopping_cart_badge')
            assert cart_count is None
        
        else:
            if username == "locked_out_user":
                error_message_element = page.get_by_text("Epic sadface:")
                assert error_message_element.is_visible()
       
@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    # "problem_user",
    "performance_glitch_user",
    "error_user",  
    "visual_user"
])        
def test_sort_products(browser_context,username):
        page = browser_context.new_page()

        # Navigate to the site
        page.goto("https://www.saucedemo.com/")

        page.get_by_placeholder('Username').fill(username)
        page.get_by_placeholder('Password').fill('secret_sauce')
        page.get_by_role('button', name='Login').click()
        if username in ["standard_user", "problem_user", "performance_glitch_user", "visual_user,error_user"]:
            assert page.locator("[data-test='inventory-container']").is_visible()
            
            # Test Case 1: Name (A to Z)
            page.locator("[data-test=\"product-sort-container\"]").select_option("az")
            product_names = page.locator(".inventory_item_name").all_inner_texts()
            assert product_names == sorted(product_names), f"Products not sorted by Name (A to Z). Found: {product_names}"

        # Test Case 2: Name (Z to A)
            page.locator("[data-test=\"product-sort-container\"]").select_option("za")
            product_names = page.locator(".inventory_item_name").all_inner_texts()
            assert product_names == sorted(product_names, reverse=True), f"Products not sorted by Name (Z to A). Found: {product_names}"

        # Test Case 3: Price (Low to High)
            page.locator("[data-test=\"product-sort-container\"]").select_option("lohi")
            product_prices = page.locator(".inventory_item_price").all_inner_texts()
            prices = [float(price.replace("$", "")) for price in product_prices]
            assert prices == sorted(prices), f"Products not sorted by Price (Low to High). Found: {prices}"

        # Test Case 4: Price (High to Low)
            page.locator("[data-test=\"product-sort-container\"]").select_option("hilo")
            product_prices = page.locator(".inventory_item_price").all_inner_texts()
            prices = [float(price.replace("$", "")) for price in product_prices]
            assert prices == sorted(prices, reverse=True), f"Products not sorted by Price (High to Low). Found: {prices}"

            print("All sorting test cases passed successfully!")
        
        else:
            if username == "locked_out_user":
                error_message_element = page.get_by_text("Epic sadface:")
                assert error_message_element.is_visible()