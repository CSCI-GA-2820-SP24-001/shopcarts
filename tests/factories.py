"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger, FuzzyDecimal
from datetime import date
from service.models.shopcart import Shopcart
from service.models.item import Item


class ShopcartFactory(factory.Factory):
    """Creates the fake shopcarts that you have to fill up with products"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Shopcart

    id = factory.Sequence(lambda n: n)
    user_id = FuzzyInteger(1, 1000)
    creation_date = FuzzyDate(date(2008, 1, 1))
    last_updated = creation_date
    total_price = 0

    @factory.post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Item

    id = factory.Sequence(lambda n: n)
    cart_id = None
    product_name = FuzzyChoice(choices=["iPhone", "MacBook Pro", "MacBook Air", "iPad"])
    product_id = FuzzyInteger(1, 1000)
    product_price = FuzzyDecimal(1.5, 2000)
    quantity = FuzzyInteger(1, 10)
