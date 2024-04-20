"""
Test cases for my Shopcart model
"""

import os
import logging
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import DataValidationError, db, Shopcart
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
        self.assertEqual(len(serial_shopcart["items"]), 1)
        items = serial_shopcart["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["cart_id"], item.cart_id)
        self.assertEqual(items[0]["product_id"], item.product_id)
        self.assertEqual(items[0]["product_price"], item.product_price)
        self.assertEqual(items[0]["quantity"], item.quantity)

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
        self.assertEqual(new_item.product_id, item.product_id)
        self.assertEqual(new_item.product_price, item.product_price)
        self.assertEqual(new_item.quantity, item.quantity)

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
        item.quantity = 2
        item.product_price = 10
        item.create()
        self.assertEqual(len(shopcart.items), 1)
        self.assertEqual(shopcart.get_total_price(), Decimal("20.0"))

    def test_find_by_user_id(self):
        """It should Find a Shopcart by total price"""
        shopcarts = ShopcartFactory.create_batch(10)
        for shopcart in shopcarts:
            shopcart.create()
        user_id = shopcarts[0].user_id
        count = len([shopcart for shopcart in shopcarts if shopcart.user_id == user_id])
        found = Shopcart.find_by_user_id(user_id)
        self.assertEqual(found.count(), count)
        for shopcart in found:
            self.assertEqual(shopcart.user_id, user_id)


######################################################################
#  T E S T   S H O P C A R T S   E X C E P T I O N   H A N D L E R S
######################################################################
class TestShopcartExceptionHandlers(TestCase):
    """Shopcart Model Exception Handlers"""

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
