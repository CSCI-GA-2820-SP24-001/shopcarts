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
        except DataValidationError:
            pass
        self.assertIsNotNone(item.product_price)

    def test_quantity_is_none(self):
        """It should not set the quantity to None"""
        item = ItemFactory()
        try:
            item.quantity = None
        except DataValidationError:
            pass
        self.assertIsNotNone(item.quantity)

    def test_repr_item(self):
        """It should be returning the representation of an item."""
        item = Item()
        item.id = 22
        item.product_name = "Foo"
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

    def test_deserialize_item(self):
        """It should be deserializinng the item properly."""
        data_to_deserealize = {
            "id": 22,
            "product_name": "Foo",
            "cart_id": 1,
            "product_id": 2,
            "product_price": 10,
            "quantity": 2,
            "subtotal": 20,
        }
        item = Item()
        deserialized_item = item.deserialize(data_to_deserealize)

        self.assertEqual(deserialized_item.product_name, "Foo")
        self.assertEqual(deserialized_item.cart_id, 1)
        self.assertEqual(deserialized_item.product_id, 2)
        self.assertEqual(deserialized_item.product_price, 10)
        self.assertEqual(deserialized_item.quantity, 2)
        self.assertEqual(deserialized_item.subtotal, 20)

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
