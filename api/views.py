from rest_framework.views import APIView
from rest_framework.response import Response

from decimal import Decimal
from math import floor


class PaymentRoundingView(APIView):
    def post(self, request):
        # Separate categories and count their prices

        categories = {}

        for invoice in request.data['invoice_lines']:
            price = Decimal(invoice['unit_price_net']) * invoice['quantity']

            if invoice['category'] in categories:
                categories[invoice['category']] += price

            else:
                categories[invoice['category']] = price

        # Generate bookkeeping data

        payment_data = []
        total_price = Decimal(sum(categories.values()))

        for count, payment in enumerate(request.data['payments']):
            data = {'id': count + 1, 'categorisations': []}

            for category in categories:
                net_amount = Decimal(payment['amount']) / total_price * categories[category]
                floored = floor(net_amount * 100) / 100.0

                data['categorisations'].append({
                    'category': category,
                    'net_amount': f'{floored:.2f}'
                })

            payment_data.append(data)

        return Response(payment_data)
