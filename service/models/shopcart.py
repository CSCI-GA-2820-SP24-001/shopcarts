"""
Models for Shopcarts and ShopcartItems

All of the models are stored in this module
"""

import logging
from datetime import datetime
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
    creation_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    last_updated = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    items = db.relationship("Item", backref="shopcart", passive_deletes=True)
    _total_price = db.Column(
        "total_price", db.Numeric(precision=10, scale=2), default=0, nullable=False
    )

    @property
    def total_price(self):
        """Returning the total price."""
        self._total_price = 0
        for item in self.items:
            self._total_price += item.subtotal
        return self._total_price

    def __repr__(self):
        return f"<Shopcart of a user with an id: {self.user_id}, exists under id=[{self.id}]>"

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating shopcart for user ID: %s", self.user_id)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving user %s's shopcart.", self.user_id)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Shopcart from the data store"""
        logger.info("Deleting %s's shopcart", self.user_id)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

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
