"""
Shopcarts Steps

Steps file for shopcarts.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@given("the following shopcarts")
def step_impl(context):
    """Delete all shopcarts and load new ones"""

    # List all shopcarts and delete them one by one
    rest_endpoint = f"{context.base_url}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK
    for shopcart in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{shopcart['id']}")
        assert context.resp.status_code == HTTP_204_NO_CONTENT

    # Load the database with new shopcarts
    for row in context.table:
        payload = {"user_id": row["user_id"], "items": []}
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED


@given("the following items")
def step_impl(context):
    """Delete all cart items and load new ones"""

    rest_endpoint = f"{context.base_url}/shopcarts"
    context.resp = requests.get(rest_endpoint)
    assert context.resp.status_code == HTTP_200_OK

    shopcarts = {}
    for shopcart in context.resp.json():
        shopcarts[shopcart["user_id"]] = shopcart["id"]

    # Load the database with new shopcarts
    for row in context.table:
        user_id = row["user_id"]
        shopcart_id = int(shopcarts[user_id])
        payload = {
            "cart_id": shopcart_id,
            "product_name": row["product_name"],
            "product_id": row["product_id"],
            "product_price": row["product_price"],
            "quantity": row["quantity"],
        }

        rest_endpoint = f"{context.base_url}/shopcarts/{shopcart_id}/items"
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED
