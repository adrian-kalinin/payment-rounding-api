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


def _distribute_amounts(available: int, prices: list):
    """
    This function distributes total amount into categories in proportion to their prices.

    :param available: total amount of payment
    :param prices: a list of prices
    :return: a list of proportionally distributed amounts
    """

    distributed_amounts = []
    total_price = sum(prices)

    for price in prices:
        distributed_amount = round(price / total_price * available)
        distributed_amounts.append(distributed_amount)

        total_price -= price
        available -= distributed_amount

    return distributed_amounts


def generate_bookkeeping_data(payments: dict, categories: dict):
    """
    This function generates bookkeeping data based on categories and payments. Integer cents are converted into
    decimal euros.

    :param payments: a dict of payments
    :param categories: a dict of categories with their prices
    :return: a dict of bookkeeping data
    """

    payment_data = []
    distributed = {category: 0 for category in categories}  # How much money is distributed to each category

    # Iterate over each payment
    for count, payment in enumerate(payments):
        data = {'id': count + 1, 'categorisations': []}

        total_price = sum(categories.values())
        available = payment['amount']

        for category, price in categories.items():
            distributed_amount = round(price / total_price * available)

            # Check if sum already distributed amount and current distributed amount is enough for the price
            if distributed[category] + distributed_amount >= price:
                distributed_amount = price - distributed[category]

            distributed[category] += distributed_amount
            available -= distributed_amount
            total_price -= price

            data['categorisations'].append({
                'category': category,
                'net_amount': f'{distributed_amount / 100:.2f}'
            })

        payment_data.append(data)

    return payment_data
