# pylint: disable=C0114
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import DataValidationError, db, Item
from .factories import ShopcartFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


class TestItems(TestCase):
    """Test Cases for Items Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # pylint: disable=R0801
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
        found = Item.all(shopcart_resource.id)
        self.assertEqual(found.count(), 1)
        data = Item.find(item_resource.id)
        self.assertEqual(data.product_id, item_resource.product_id)

    def test_quantity_is_not_none(self):
        """It should calculate the subtotal if the quantity is not None"""
        item = ItemFactory()
        item.quantity = 2
        item.product_price = 10
        self.assertEqual(item.get_subtotal(), 20.0)

    def test_repr_item(self):
        """It should be returning the representation of an item."""
        item = Item()
        item.id = 22
        item.product_name = "Foo"
        self.assertEqual("<Item Foo with id=[22]>", str(item))

    def test_serialize_an_item(self):
        """It should serialize an Item"""
        item = ItemFactory()
        serial_item = item.serialize()
        self.assertEqual(serial_item["id"], item.id)
        self.assertEqual(serial_item["product_name"], item.product_name)
        self.assertEqual(serial_item["cart_id"], item.cart_id)
        self.assertEqual(serial_item["product_id"], item.product_id)
        self.assertEqual(serial_item["product_price"], item.product_price)
        self.assertEqual(serial_item["quantity"], item.quantity)

    def test_deserialize_an_item(self):
        """It should deserialize an Item"""
        item = ItemFactory()
        new_item = Item()
        new_item.deserialize(item.serialize())
        self.assertEqual(new_item.cart_id, item.cart_id)
        self.assertEqual(new_item.product_name, item.product_name)
        self.assertEqual(new_item.product_id, item.product_id)
        self.assertEqual(new_item.product_price, item.product_price)
        self.assertEqual(new_item.quantity, item.quantity)

    def test_deserialize_errors(self):
        """It should raise an error if the data is not correct."""
        item = Item()
        item.id = 22
        item.product_name = "Foo"
        self.assertRaises(
            DataValidationError, item.deserialize, {"id": 22, "product_name": "Foo"}
        )

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_list_items_in_the_shopcart(self):
        """It should be filtering and listing items in the shopcart."""
        shopcart = ShopcartFactory()
        shopcart.create()

        item1 = ItemFactory(shopcart=shopcart)
        item1.create()

        item2 = ItemFactory(shopcart=shopcart)
        item2.create()

        items = Item.all(shopcart.id)
        for item in items:
            self.assertEqual(item.cart_id, shopcart.id)

        # If the randomizer generated two different product_IDs for the items, we take item1
        if item1.product_id != item2.product_id:
            product_id = item1.product_id
            quantity = item1.quantity
        # If the randomizer generated the same product_ID for the items, we take any of the product_IDs
        else:
            product_id = item2.product_id
            quantity = item2.quantity

        self.assertNotEqual(Item.find_by_product_id(product_id).count(), 0)
        self.assertNotEqual(Item.find_by_quantity(quantity).count(), 0)
        self.assertEqual(items.count(), 2)


######################################################################
#  T E S T   I T E M S   E X C E P T I O N   H A N D L E R S
######################################################################
class TestItemExceptionHandlers(TestCase):
    """Item Model Exception Handlers"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # pylint: disable=R0801
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

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        item = Item()
        self.assertRaises(DataValidationError, item.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        item = Item()
        self.assertRaises(DataValidationError, item.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        item = Item()
        self.assertRaises(DataValidationError, item.delete)
