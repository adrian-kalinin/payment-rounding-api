def separate_categories(invoice_lines: dict):
    """
    This function separates categories and counts their prices. Decimal euros are converted into integer cents.

    :param invoice_lines: dictionary with invoice lines
    :return: dictionary with separated categories
    """

    categories = {}

    for invoice in invoice_lines:
        price = int(invoice['unit_price_net'].replace('.', '')) * invoice['quantity']

        if invoice['category'] in categories:
            categories[invoice['category']] += price
        else:
            categories[invoice['category']] = price

    return categories


def prepare_payment_data(payments):
    """
    This function converts decimal euros into integer cents in the list of payments.

    :param payments: a list of raw payments
    :return: a list of converted payments
    """

    for payment in payments:
        converted_amount = int(payment['amount'].replace('.', ''))
        payment['amount'] = converted_amount

    return payments


def _distribute_amounts(available: int, categories: dict, distributed_by_categories: dict):
    """
    This function distributes total amount into categories in proportion to their prices. Integer cents are converted
    into decimal euros.

    :param available: amount of available money from a payment
    :param categories: a dict of categories with their prices
    :param distributed_by_categories: a dict of distributed categories
    :return: a list of proportionally distributed amounts
    """

    data = []
    total_price = sum(categories.values())

    for category, price in categories.items():
        distributed_amount = round(price / total_price * available)

        # Check if sum of already distributed amount and current distributed amount is enough for the price
        if distributed_by_categories[category] + distributed_amount >= price:
            distributed_amount = price - distributed_by_categories[category]

        distributed_by_categories[category] += distributed_amount
        total_price -= price
        available -= distributed_amount

        data.append({
            'category': category,
            'net_amount': f'{distributed_amount / 100:.2f}'
        })

    return data, distributed_by_categories


def generate_bookkeeping_data(payments: list, categories: dict):
    """
    This function generates bookkeeping data based on categories and payments.

    :param payments: a list of payments
    :param categories: a dict of categories and their prices
    :return: a dict of bookkeeping data
    """

    payment_data = []

    # How much money is already distributed to each category
    distributed_by_categories = {category: 0 for category in categories}

    for payment in payments:
        categorisations, distributed_by_categories = _distribute_amounts(
            payment['amount'], categories, distributed_by_categories
        )

        payment_data.append({
            'id': payment['id'],
            'categorisations': categorisations
        })

    return payment_data
