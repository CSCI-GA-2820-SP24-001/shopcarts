"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import DataValidationError, db, Shopcart, Item
from .factories import ShopcartFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Shopcarts   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestShopcarts(TestCase):
    """Test Cases for Shopcarts Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_shopcarts(self):
        """It should create a Shopcarts"""
        resource = ShopcartFactory()
        resource.create()
        self.assertIsNotNone(resource.id)
        found = Shopcart.all()
        self.assertEqual(len(found), 1)
        data = Shopcart.find(resource.id)
        self.assertEqual(data.user_id, resource.user_id)

    def test_shopcart_serialization(self):
        """It should properly serialize the shopcart."""
        resource = ShopcartFactory(
            id=21,
            user_id="101",
            creation_date="2024-01-01",
            last_updated="2024-01-01",
        )

        print(resource.serialize())
        dictionary_data = resource.serialize()
        ground_truth_data = {
            "id": 21,
            "user_id": "101",
            "creation_date": "2024-01-01",
            "last_updated": "2024-01-01",
            "total_price": 0,
            "items": [],
        }
        self.assertDictEqual(dictionary_data, ground_truth_data)


class TestItems(TestCase):
    """Test Cases for Shopcarts Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_items(self):
        """It should create an Item in the Shopcart"""
        shopcart_resource = ShopcartFactory()
        shopcart_resource.create()

        item_resource = ItemFactory(shopcart=shopcart_resource)
        item_resource.create()

        self.assertIsNotNone(item_resource.id)
        found = Item.all()
        self.assertEqual(len(found), 1)
        data = Item.find(item_resource.id)
        self.assertEqual(data.product_id, item_resource.product_id)

    def test_quantity_is_not_none(self):
        """It should calculate the subtotal if the quantity is not None"""
        item = ItemFactory()
        item.quantity = 2
        item.product_price = 10
        self.assertEqual(item.subtotal, 20.0)

    def test_product_price_is_none(self):
        """It should not set the product_price to None"""
        item = ItemFactory()
        try:
            item.product_price = None
            self.assertTrue(False)
        except DataValidationError:
            self.assertTrue(True)

    def test_quantity_is_none(self):
        """It should not set the quantity to None"""
        item = ItemFactory()
        try:
            item.quantity = None
            self.assertTrue(False)
        except DataValidationError:
            self.assertTrue(True)

    def test_repr_item(self):
        """It should be returning the representation of an item."""
        item = Item(product_name="Foo", id=22)
        self.assertEqual("<Item Foo with id=[22]>", str(item))

    def test_serialize_item(self):
        """It should properly serialize the item."""
        item = ItemFactory(
            id=22,
            product_name="Foo",
            cart_id=1,
            product_id=2,
            product_price=10,
            quantity=2,
            subtotal=20,
        )

        dictionary_data = item.serialize()
        ground_truth_data = {
            "id": 22,
            "product_name": "Foo",
            "cart_id": 1,
            "product_id": 2,
            "product_price": 10,
            "quantity": 2,
            "subtotal": 20,
        }
        self.assertDictEqual(dictionary_data, ground_truth_data)
