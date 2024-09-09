from playwright.sync_api import Page

import pytest


# @pytest.mark.skip_browser("chromium")
# @pytest.mark.only_browser("chromium")
def test_title(page:Page):
    page.goto("https://www.saucedemo.com")
    assert page.title() == "Swag Labs"
    
    
def test_inventory_site(page:Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.inner_text("h3") == "Epic sadface: You can only access '/inventory.html' when you are logged in."
    


def test_inventory_price(page:Page):
    page.goto("https://www.saucedemo.com/v1/inventory-item.html?id=4")
    price = page.inner_text(".inventory_details_price")
    assert price== "$29.99"
    
# def test_inventory_price(page:Page):
#     page.goto("https://www.saucedemo.com/v1/cart.html")
#     desc = page.inner_text("inventory_item_desc")
#     assert desc== "$29.99"