from django.test import TestCase
from copy import deepcopy

from .utils.bookkeeping import distribute_amounts


class DistributingTests(TestCase):
    # There is sample data below
    categories = {'a': 15, 'b': 20, 'c': 35}
    distributed_by_categories = {'a': 0, 'b': 0, 'c': 0}
    total_price = sum(categories.values())

    def test_distributed_is_less_or_equal_total_price(self):
        """
        Tests whether sum of distributed amounts is less or equal total price. Thus we do not distribute extra
        much money.
        """

        for available in range(100):
            data, _ = distribute_amounts(available, deepcopy(self.categories), deepcopy(self.distributed_by_categories))
            total_distributed = sum([category['net_amount'] for category in data])

            self.assertLessEqual(total_distributed, self.total_price)

    def test_distributed_equals_available_or_total_price(self):
        """
        Tests whether sum of distributed amounts equals available amount or total price. Thus we distribute exact
        needed amount of money.
        """

        for available in range(100):
            data, _ = distribute_amounts(available, deepcopy(self.categories), deepcopy(self.distributed_by_categories))
            total_distributed = sum([category['net_amount'] for category in data])

            if available < self.total_price:
                self.assertEqual(total_distributed, available)
            else:
                self.assertEqual(total_distributed, self.total_price)

    def test_each_distributed_amount_is_less_or_equal_price(self):
        """
        Tests whether each distributed amount is less or equal original category's price. Thus we distribute the
        right amount of money to each category.
        """

        for available in range(100):
            data, _ = distribute_amounts(available, deepcopy(self.categories), deepcopy(self.distributed_by_categories))

            for categorisation in data:
                category = categorisation['category']

                self.assertLessEqual(categorisation['net_amount'], self.categories[category])
