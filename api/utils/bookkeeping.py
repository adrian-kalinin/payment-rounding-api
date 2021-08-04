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
    distributed = {category: 0 for category in categories}

    # Iterate over each payment
    for count, payment in enumerate(payments):
        data = {'id': count + 1, 'categorisations': []}

        total_price = sum(categories.values())
        available = int(payment['amount'].replace('.', ''))  # Convert decimal euros into integer cents

        # Iterate over each category and distribute money from payment
        for category, price in categories.items():
            distributed_amount = round(price / total_price * available)

            # Check if already distributed amount and current distributed amount are enough for the price
            if distributed[category] + distributed_amount >= price:
                distributed_amount = price - distributed[category]

            amount_euros = f'{distributed_amount / 100:.2f}'  # Convert integer cents into decimal euros
            distributed[category] += distributed_amount
            available -= distributed_amount
            total_price -= price

            data['categorisations'].append({
                'category': category,
                'net_amount': amount_euros
            })

        payment_data.append(data)

        print([float(d) / 100 for d in distributed.values()], [float(price) / 100 for price in categories.values()])

    return payment_data
