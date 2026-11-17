"""Tests unitaires des règles de prix — POINT DE DÉPART (Atelier 1).

Complétez ce fichier : objectif >= 90 % de couverture sur minishop/pricing.py.
"""

from decimal import Decimal

import pytest

from minishop.pricing import line_total, money, quote

pytestmark = pytest.mark.unit


def test_money_arrondi_commercial():
    """0.125 s'arrondit à 0.13 (ROUND_HALF_UP), pas 0.12."""
    assert money("0.125") == Decimal("0.13")


def test_line_total_sans_remise():
    assert line_total(Decimal("12.50"), 2) == Decimal("25.00")


def test_quote_panier_vide():
    """Un panier vide coûte 0 € : pas de frais de livraison."""
    q = quote([])
    assert q.total == Decimal("0.00")
    assert q.shipping == Decimal("0.00")

def test_line_total_remise_volume():
    assert line_total(Decimal("10.00"), 10) == Decimal("95.00")
    assert line_total(Decimal("10.00"), 9) == Decimal("90.00")

@pytest.mark.parametrize("qty", [0, -1, 100, "2", True])
def test_quantite_invalide(qty):
    with pytest.raises(ValueError):
        line_total(Decimal("10"), qty)

def test_coupon_freeship_panier_vide():
    assert shipping_cost(None, None, True) == Decimal("0.00")

def test_coupons_seuil():
    assert coupon_discount(Decimal("20.00"), "WELCOME10") == Decimal("2.00")
    assert coupon_discount(Decimal("30.00"), "FIXED5") == Decimal("5.00")

def test_coupons_exclus():
    assert coupon_discount(Decimal("19.99"), "WELCOME10") == Decimal("0.00")
    assert coupon_discount(Decimal("29.99"), "FIXED5") == Decimal("0.00")

def test_coupons_inconnus():
    with pytest.raises(ValueError):
        coupon_discount(Decimal("20.00"), "EXAMPLE") 
        coupon_discount(Decimal("30.00"), "EXAMPLE")

def test_coupon_freeship_inconnu()
    assert shipping_cost(Decimal("49.99"), "EXAMPLE", False) == Decimal("4.90")

def test_coupons_upercase():
    assert coupon_discount(Decimal("20.00"), "welcome10") == Decimal("2.00")
    assert coupon_discount(Decimal("30.00"), "fixed5") == Decimal("5.00")

def test_coupon_freeship_uppercase()
    assert shipping_cost(Decimal("10.00"), "freeship", False) == Decimal("0.00")

def test_coupon_freeship_seuil():
    assert shipping_cost(Decimal("50.00"), None, False) == Decimal("0.00")
    
def test_coupon_
    assert coupon_discount(Decimal("50.00"), None) == Decimal("0.00")
    assert coupon_discount(Decimal("50.00"), "") == Decimal("0.00")

# TODO Atelier 1 :
#  - remise volume à partir de 10 unités (et pas à 9 !)
#  - quantités invalides (0, 100, -1, "2", True) -> ValueError   (astuce : @pytest.mark.parametrize)
#  - coupons WELCOME10 / FIXED5 / FREESHIP (seuils inclus/exclus), coupon inconnu, casse
#  - livraison offerte à partir de 50 € APRÈS remise
#  - produit inconnu -> KeyError
