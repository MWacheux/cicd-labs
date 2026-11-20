"""Test E2E Playwright — POINT DE DÉPART (Atelier 8).

Prérequis : application lancée (make run) ; BASE_URL=http://localhost:8000 par défaut.
Lancer :   pytest -m e2e --headed        (pour voir le navigateur)
"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.shop_page import ShopPage

@pytest.fixture
def shop(page: Page, app_url) -> ShopPage:
    page.goto(app_url)
    return ShopPage(page)


def test_page_accueil(shop: ShopPage):
    expect(shop.page).to_have_title(re.compile("MiniShop"))
    expect(shop.page.get_by_test_id("products").locator("li")).to_have_count(5)


def test_parcours_commande_confirmee(shop: ShopPage):

    shop.add("mug").add("mug")
    shop.apply_coupon("WELCOME10")

    expect(shop.page.get_by_test_id("order-btn")).to_be_enabled()
    assert shop.total() != ""

    confirmation = shop.order()
    expect(confirmation).to_contain_text("Commande")


def test_parcours_achat_coupon_invalide(shop: ShopPage):

    shop.add("mug").add("mug")
    shop.apply_coupon("WELCOM1")

    expect(shop.page.get_by_role("alert")).to_be_visible()

def test_commander_desactivee_si_panier_vide(shop: ShopPage):
    order_button = shop.page.get_by_test_id("order-btn")
    expect(shop.page.get_by_test_id("cart")).to_contain_text("Votre panier est vide")
    expect(order_button).to_be_disabled()

    shop.add("mug")
    expect(order_button).to_be_enabled()





