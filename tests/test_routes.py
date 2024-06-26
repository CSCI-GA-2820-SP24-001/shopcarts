"""
TestShopcarts API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import Shopcart
from service.models.persistent_base import db
from .factories import ShopcartFactory, ItemFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/shopcarts"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestShopcartService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        # pylint: disable=R0801
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_shopcarts(self, count):
        """Factory method to create shopcarts in bulk"""
        shopcarts = []
        for _ in range(count):
            test_shopcart = ShopcartFactory()
            response = self.client.post(BASE_URL, json=test_shopcart.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test shopcart",
            )
            new_shopcart = response.get_json()
            test_shopcart.id = new_shopcart["id"]
            shopcarts.append(test_shopcart)
        return shopcarts

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_shopcart(self):
        """It should Create a new Shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug("Test Shopcart: %s", test_shopcart.serialize())
        response = self.client.post(BASE_URL, json=test_shopcart.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_shopcart = response.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id)
        self.assertEqual(new_shopcart["items"], test_shopcart.items)

        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_shopcart = response.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id)
        self.assertEqual(new_shopcart["items"], test_shopcart.items)

    def test_get_shopcart(self):
        """It should Get a single Shopcart"""
        # get the id of a shopcart
        test_shopcart = self._create_shopcarts(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_shopcart.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["user_id"], test_shopcart.user_id)

    def test_update_shopcart(self):
        """It should Update an existing Shopcart"""
        # create a shopcart to update
        test_shopcart = ShopcartFactory()
        response = self.client.post(BASE_URL, json=test_shopcart.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # update the shopcart
        new_shopcart = response.get_json()
        logging.debug(new_shopcart)
        new_shopcart["user_id"] = "123"
        # test that we cannot update a shopcart with the shopcart id that DNE
        response = self.client.put(f"{BASE_URL}/0", json=new_shopcart)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # test that we can actually update the desired shopcart when needed
        response = self.client.put(
            f"{BASE_URL}/{new_shopcart['id']}", json=new_shopcart
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_shopcart = response.get_json()
        self.assertEqual(updated_shopcart["user_id"], "123")

    def test_delete_shopcart(self):
        """It should Delete a Shopcart"""
        test_shopcart = self._create_shopcarts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_shopcart.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_shopcart.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_shopcart_list(self):
        """It should Get a list of Shopcarts"""
        self._create_shopcarts(5)

        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

        shopcart = data[0]
        shopcart_user_id = shopcart["user_id"]

        resp = self.client.get(f"{BASE_URL}?user_id={shopcart_user_id}")
        data = resp.get_json()
        self.assertNotEqual(len(data), 0)

    def test_add_item(self):
        """It should Add an item to a shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        item.cart_id = None
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["product_name"], item.product_name)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["product_price"], str(item.product_price))

    def test_shopcart_not_found(self):
        """It should not find a shopcart"""
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/0/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item(self):
        """It should Get an item from a shopcart"""
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["product_name"], item.product_name)
        self.assertEqual(data["cart_id"], shopcart.id)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["product_price"], str(item.product_price))

    def test_update_shopcart_item(self):
        """It should Update an existing item in a Shopcart"""
        # create a shopcart with an item to update
        # create a shopcart and an item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        product_name = data["product_name"]
        item_id = data["id"]

        # test for the shopcart ID being invalid
        resp = self.client.put(
            f"{BASE_URL}/0/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        dummy_item_id = item_id + 1
        shopcart_id = shopcart.id
        # test for the item ID being invalid
        resp = self.client.put(
            f"{BASE_URL}/{shopcart_id}/items/{dummy_item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        data["product_name"] = "Updated Item Name"

        # send the update back
        response = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve it back
        response = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertNotEqual(data["product_name"], product_name)

    def test_delete_item(self):
        """It should Delete an Item"""
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_list(self):
        """It should Get a list of items in a shopcart"""
        # add four items to the shopcart
        shopcart = self._create_shopcarts(1)[0]
        item_list = ItemFactory.create_batch(4)

        # create items
        for item in item_list:
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.id}/items", json=item.serialize()
            )
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.get(f"{BASE_URL}/{shopcart.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 4)

        product_id = data[0]["product_id"]
        quantity = data[0]["quantity"]

        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items?product_id={product_id}"
        )
        data = resp.get_json()
        self.assertNotEqual(len(data), 0)

        resp = self.client.get(f"{BASE_URL}/{shopcart.id}/items?quantity={quantity}")
        data = resp.get_json()
        self.assertNotEqual(len(data), 0)

        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items?product_id={product_id}&quantity={quantity}"
        )
        data = resp.get_json()
        self.assertNotEqual(len(data), 0)

    def test_clear_shopcart(self):
        """Test clearing all items in a shopcart"""
        # Create a shopcart with items
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()

        # Add item to shopcart
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Send request to clear shopcart
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}/clear",
            content_type="application/json",
        )

        # Check response status code
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(resp.data, b"")

        resp = self.client.delete(
            f"{BASE_URL}/0/clear",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_increment_quantity_by_one(self):
        """It should increment quantity by one"""
        # add four items to the shopcart
        # create a shopcart and an item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        # let's commit the newly created item to the DB
        initial_quantity = item.quantity
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.json
        item_id = data["id"]

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}/increment", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json
        new_quantity = data["quantity"]
        self.assertEqual(new_quantity, initial_quantity + 1)

        resp = self.client.put(
            f"{BASE_URL}/0/items/{item.id}/increment", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/0/increment", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_decrement_quantity_by_one(self):
        """It should decrement quantity by one"""
        # add four items to the shopcart
        # create a shopcart and an item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        # let's commit the newly created item to the DB
        initial_quantity = item.quantity
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.json
        item_id = data["id"]

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}/decrement", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json
        new_quantity = data["quantity"]
        self.assertEqual(new_quantity, initial_quantity - 1)

        resp = self.client.put(
            f"{BASE_URL}/0/items/{item.id}/decrement", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/0/decrement", json=item.serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_create_shopcart_no_data(self):
        """It should not Create a Shopcart with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_shopcart_not_found(self):
        """It should not Get a Shopcart that's not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_create_shopcart_no_content_type(self):
        """It should not Create a Shopcart with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_shopcart_wrong_content_type(self):
        """It should not Create a Shopcart with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_get_shopcart_with_method_not_allowed(self):
        """It should not allow us to get a Shopcart with the method that is not allowed"""
        test_shopcart = ShopcartFactory()
        response = self.client.post(f"{BASE_URL}/{test_shopcart.id}")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_items_when_shopcart_not_found(self):
        """It should not Get any items from a shopcart that's not found"""
        response = self.client.get(f"{BASE_URL}/0/items")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])
