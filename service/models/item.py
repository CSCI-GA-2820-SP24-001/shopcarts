"""
Model for Items

All of the models are stored in this module
"""

import logging
from .persistent_base import db, PersistentBase, DataValidationError


logger = logging.getLogger("flask.app")


# pylint: disable=too-many-instance-attributes
class Item(db.Model, PersistentBase):
    """
    Class that represents an item in the shopcart.
    """

    ##################################################
    # Table Schema
    ##################################################

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(63))
    cart_id = db.Column(
        db.Integer, db.ForeignKey("shopcart.id", ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(db.Integer)
    product_price = db.Column(
        "product_price", db.Numeric(precision=10, scale=2), nullable=False, default=0
    )
    quantity = db.Column("quantity", db.Integer, nullable=False, default=0)

    def get_subtotal(self):
        """Return the subtotal."""
        return self.product_price * self.quantity

    def __repr__(self):
        return f"<Item {self.product_name} with id=[{self.id}]>"

    def serialize(self):
        """Serializes a Item into a dictionary"""
        return {
            "id": self.id,
            "product_name": self.product_name,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "product_price": self.product_price,
            "quantity": self.quantity,
            "subtotal": self.get_subtotal(),
        }

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.cart_id = data["cart_id"]
            self.product_name = data["product_name"]
            self.product_id = data["product_id"]
            self.product_price = data["product_price"]
            self.quantity = data["quantity"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################
    @classmethod
    def all(cls) -> list:
        """Returns all of the Items in the database"""
        logger.info("Processing all Items and returning them as a list ...")
        return cls.query.all()

    @classmethod
    def find_by_product_id(cls, product_id) -> list:
        """Returns all Items in the Shopcart associated with the given product_id

        Args:
            product_id (int): the product_id of the Items you want to match belongs to
        """
        logger.info(
            "Processing items query for the product with an ID: %s ...", product_id
        )
        return cls.query.filter(cls.product_id == product_id)

    @classmethod
    def find_by_quantity(cls, quantity) -> list:
        """Returns all Items in the Shopcart associated with the given quantity

        Args:
            quantity (int): the quantity of the Items you want to match belongs to
        """
        logger.info("Processing items query which have a quantity of: %s ...", quantity)
        return cls.query.filter(cls.quantity == quantity)
