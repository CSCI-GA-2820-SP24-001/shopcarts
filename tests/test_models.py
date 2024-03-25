"""
Test cases for my Models
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
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

    def test_add_a_shopcart(self):
        """It should create a Shopcarts"""
        resource = ShopcartFactory()
        resource.create()
        self.assertIsNotNone(resource.id)
        self.assertIsNotNone(resource.creation_date)
        self.assertIsNotNone(resource.last_updated)
        found = Shopcart.all()
        self.assertEqual(len(found), 1)
        data = Shopcart.find(resource.id)
        self.assertEqual(data.user_id, resource.user_id)
        self.assertEqual(data.total_price, 0)

    def test_read_a_shopcart(self):
        """It should Read a Shopcart"""
        shopcart = ShopcartFactory()
        logging.debug(shopcart)
        shopcart.id = None
        shopcart.create()
        self.assertIsNotNone(shopcart.id)
        # Fetch it back
        found_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(found_shopcart.id, shopcart.id)
        self.assertEqual(found_shopcart.user_id, shopcart.user_id)
        self.assertEqual(found_shopcart.creation_date, shopcart.creation_date)

    def test_update_a_shopcart(self):
        """It should Update a Shopcart"""
        shopcart = ShopcartFactory()
        logging.debug(shopcart)
        shopcart.id = None
        shopcart.create()
        logging.debug(shopcart)
        self.assertIsNotNone(shopcart.id)
        self.assertIsNotNone(shopcart.creation_date)
        self.assertIsNotNone(shopcart.last_updated)
        # Change it an save it
        original_id = shopcart.id
        shopcart.update()
        self.assertEqual(shopcart.id, original_id)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        self.assertEqual(shopcarts[0].id, original_id)

    def test_update_no_id(self):
        """It should not Update a Shopcart with no id"""
        shopcart = ShopcartFactory()
        logging.debug(shopcart)
        shopcart.id = None
        self.assertRaises(DataValidationError, shopcart.update)

    def test_delete_a_shopcart(self):
        """It should Delete a Shopcart"""
        shopcart = ShopcartFactory()
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        # delete the shopcart and make sure it isn't in the database
        shopcart.delete()
        self.assertEqual(len(Shopcart.all()), 0)

    def test_list_all_shopcarts(self):
        """It should List all Shopcarts in the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        # Create 5 Shopcarts
        for _ in range(5):
            shopcart = ShopcartFactory()
            shopcart.create()
        # See if we get back 5 shopcarts
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 5)

    def test_serialize_a_shopcart(self):
        """It should Serialize a shopcart"""
        shopcart = ShopcartFactory()
        item = ItemFactory()
        shopcart.items.append(item)
        serial_shopcart = shopcart.serialize()
        self.assertEqual(serial_shopcart["id"], shopcart.id)
        self.assertEqual(serial_shopcart["user_id"], shopcart.user_id)
        self.assertEqual(serial_shopcart["total_price"], shopcart.total_price)
        self.assertEqual(len(serial_shopcart["items"]), 1)
        items = serial_shopcart["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["cart_id"], item.cart_id)
        self.assertEqual(items[0]["product_id"], item.product_id)
        self.assertEqual(items[0]["product_price"], item.product_price)
        self.assertEqual(items[0]["quantity"], item.quantity)
        self.assertEqual(items[0]["subtotal"], item.subtotal)

    def test_deserialize_a_shopcart(self):
        """It should Deserialize a shopcart"""
        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.items.append(item)
        shopcart.create()

        serial_shopcart = shopcart.serialize()
        new_shopcart = Shopcart()
        new_shopcart.deserialize(serial_shopcart)
        self.assertEqual(new_shopcart.user_id, shopcart.user_id)
        self.assertEqual(len(new_shopcart.items), 1)

        new_item = new_shopcart.items[0]
        self.assertEqual(new_item.cart_id, item.cart_id)
        self.assertEqual(new_item.product_id, item.product_id)
        self.assertEqual(new_item.product_price, item.product_price)
        self.assertEqual(new_item.quantity, item.quantity)
        self.assertEqual(new_item.subtotal, item.subtotal)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an shopcart with a KeyError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an shopcart with a TypeError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, [])

    def test_add_items_to_shopcart(self):
        """It should add items to the shopcart and update the total_price."""
        shopcart = ShopcartFactory()
        shopcart.create()
        item = ItemFactory(shopcart=shopcart)
        item.create()
        self.assertEqual(len(shopcart.items), 1)
        self.assertNotEqual(shopcart.total_price, 0)

    def test_find_by_user_id(self):
        """It should Find an Shopcart by user_id"""
        shopcart = ShopcartFactory()
        shopcart.create()

        # Fetch it back by user_id
        same_shopcart = Shopcart.find_by_user_id(shopcart.user_id)[0]
        self.assertEqual(same_shopcart.id, shopcart.id)
        self.assertEqual(same_shopcart.user_id, shopcart.user_id)


class TestItems(TestCase):
    """Test Cases for Items Model"""

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
        try:
            item.deserialize({"id": 22, "product_name": "Foo"})
            self.assertTrue(False)
        except DataValidationError:
            self.assertTrue(True)

    def test_invalid_attribute(self):
        """It should raise an error if the attribute is not correct."""
        try:
            item = Item(inexistent_id="random_string", product_name="Foo")
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])


######################################################################
#  T E S T   S H O P C A R T S   E X C E P T I O N   H A N D L E R S
######################################################################
class TestShopcartExceptionHandlers(TestCase):
    """Shopcart Model Exception Handlers"""

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

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.create)

    @patch("service.models.db.session.commit")
    def test_update_shopcart_failed(self, exception_mock):
        # TODO: this one should be triggering persistent_base.py lines 75-78, but isn't
        """It should not update an Shopcart on database error"""
        exception_mock.side_effect = Exception()
        shopcart = ShopcartFactory()
        self.assertRaises(DataValidationError, shopcart.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.delete)


######################################################################
#  T E S T   S H O P C A R T S   E X C E P T I O N   H A N D L E R S
######################################################################
class TestItemExceptionHandlers(TestCase):
    """Item Model Exception Handlers"""

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
