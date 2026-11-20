"""Tests d'API — POINT DE DÉPART (Atelier 1, puis Atelier 9)."""

import httpx
import pytest

pytestmark = pytest.mark.api


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_liste_produits(client):
    r = client.get("/products")
    assert r.status_code == 200
    assert {"mug", "tshirt"} <= {p["id"] for p in r.json()}


# TODO Atelier 9 : /products/{id} (200, 404), /cart/quote (200, 404, 422), /orders (201, 422), GET /orders/{id}

def test_produit_code200(client):
    r = client.get("/products/mug")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "mug"

def test_produit_code404(client):
    r = client.get("/products/inconnu")
    assert r.status_code == 404


def test_cart_quote_code200_verifie_total(client):
    payload = {"items": [{"product_id": "mug", "qty": 2}]}
    r = client.post("/cart/quote", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == "29.90"


def test_cart_quote_code404_produit_inconnu(client):
    payload = {"items": [{"product_id": "inconnu", "qty": 1}]}
    r = client.post("/cart/quote", json=payload)
    assert r.status_code == 404


@pytest.mark.parametrize("qty", [0, 100])
def test_cart_quote_code422_quantite_hors_limites(client, qty):
    payload = {"items": [{"product_id": "mug", "qty": qty}]}
    r = client.post("/cart/quote", json=payload)
    assert r.status_code == 422


def test_cart_quote_code422_coupon_inconnu(client):
    payload = {"items": [{"product_id": "mug", "qty": 1}], "coupon": "NOPE"}
    r = client.post("/cart/quote", json=payload)
    assert r.status_code == 422


def test_cart_quote_code422_corps_invalide(client):
    r = client.post("/cart/quote", json=[])
    assert r.status_code == 422


def test_orders_code201_puis_get_meme_commande(client):
    payload = {"items": [{"product_id": "mug", "qty": 2}]}
    create = client.post("/orders", json=payload)
    assert create.status_code == 201

    order = create.json()
    order_id = order["id"]

    fetched = client.get(f"/orders/{order_id}")
    assert fetched.status_code == 200
    assert fetched.json() == order


def test_orders_code422_panier_vide(client):
    create = client.post("/orders", json={"items": []})
    assert create.status_code == 422


def test_metrics_expose_minishop_http_requests_total(client):
    client.get("/health")
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "minishop_http_requests_total" in r.text


def test_metrics_expose_minishop_http_requests_total_serveur_reel(app_url):
    try:
        with httpx.Client(base_url=app_url, timeout=5.0) as real_client:
            real_client.get("/health")
            r = real_client.get("/metrics")
    except httpx.HTTPError:
        pytest.skip("Serveur réel indisponible (Docker non lancé ?)")

    assert r.status_code == 200
    assert "minishop_http_requests_total" in r.text