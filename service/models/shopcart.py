"""
Models for Shopcarts and ShopcartItems

All of the models are stored in this module
"""

import logging
from .persistent_base import db, PersistentBase, DataValidationError
from .item import Item

logger = logging.getLogger("flask.app")


class Shopcart(db.Model, PersistentBase):
    """
    Class that represents a Shopcart
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(63))
    creation_date = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)
    items = db.relationship("Item", backref="shopcart", passive_deletes=True)
    _total_price = db.Column(
        "total_price", db.Numeric(precision=10, scale=2), nullable=False
    )

    @property
    def total_price(self):
        """Returning the total price."""
        return self._total_price

    @total_price.setter
    def total_price(self, items: list[Item]):
        """Triggered to update item quantity and recalculate subtotal."""
        self._total_price = 0
        for item in self.items:
            self.total_price += item.subtotal

    def __repr__(self):
        return f"<Shopcart of a user with an id: {self.user_id}, exists under id=[{self.id}]>"

    def serialize(self):
        """Serializes a Shopcart into a dictionary"""
        shopcart = {
            "id": self.id,
            "user_id": self.user_id,
            "creation_date": self.creation_date,
            "last_updated": self.last_updated,
            "total_price": self.total_price,
            "items": [],
        }
        for item in self.items:
            shopcart["items"].append(item.serialize())

        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.user_id = data["user_id"]
            self.creation_date = data["creation_date"]
            self.last_updated = data["last_updated"]
            self.total_price = data["total_price"]
            item_list = data.get("items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def find_by_user_id(cls, user_id):
        """Returns all Shopcarts associated with the given user_id

        Args:
            user_id (string): the user_id of the user to whom Shopcart you want to match belongs to
        """
        logger.info("Processing carts query for the user with id: %s ...", user_id)
        return cls.query.filter(cls.user_id == user_id)
