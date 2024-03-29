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
    _product_price = db.Column(
        "product_price", db.Numeric(precision=10, scale=2), nullable=False, default=0
    )
    _quantity = db.Column("quantity", db.Integer, nullable=False, default=0)
    subtotal = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    @property
    def product_price(self):
        """Returning the product price."""
        return self._product_price

    @property
    def quantity(self):
        """Returning a quantity of an item."""
        return self._quantity

    @product_price.setter
    def product_price(self, value):
        """Update item quantity and recalculate subtotal."""
        if value is not None:
            self._product_price = value
            if self.quantity:
                self.subtotal = self._product_price * self._quantity
        else:
            raise DataValidationError("Product price cannot be None")

    @quantity.setter
    def quantity(self, value):
        """Update item quantity and recalculate subtotal."""
        if value is not None:
            self._quantity = value

            if self.product_price:
                self.subtotal = self._product_price * self._quantity
        else:
            raise DataValidationError("Quantity cannot be None")

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
            "subtotal": self.subtotal,
        }

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.product_name = data["product_name"]
            self.cart_id = data["cart_id"]
            self.product_id = data["product_id"]
            self.product_price = data["product_price"]
            self.quantity = data["quantity"]
            self.subtotal = data["subtotal"]
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
