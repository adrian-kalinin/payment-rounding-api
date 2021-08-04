def separate_categories(invoice_lines):
    categories = {}

    # Iterate over each invoice line
    for invoice in invoice_lines:
        price = int(invoice['unit_price_net'].replace('.', '')) * invoice['quantity']

        if invoice['category'] in categories:
            categories[invoice['category']] += price
        else:
            categories[invoice['category']] = price

    return categories


def generate_bookkeeping_data(payments, categories):
    payment_data = []

    # Iterate over each payment
    for count, payment in enumerate(payments):
        data = {'id': count + 1, 'categorisations': []}

        total_price = sum(categories.values())
        available = int(payment['amount'].replace('.', ''))  # Convert decimal euros into integer cents

        # Iterate over each category and distribute money from payment
        for category, price in categories.items():
            distributed_amount = round(price / total_price * available)

            if price <= distributed_amount:
                distributed_amount = price

            amount_euros = f'{distributed_amount / 100:.2f}'  # Convert integer cents into decimal euros
            available -= distributed_amount
            total_price -= price

            data['categorisations'].append({
                'category': category,
                'net_amount': amount_euros
            })

        payment_data.append(data)

    return payment_data
