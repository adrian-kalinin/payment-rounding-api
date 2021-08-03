from rest_framework.views import APIView
from rest_framework.response import Response

from decimal import Decimal


class PaymentRoundingView(APIView):
    def post(self, request):
        # Separate categories and count their prices

        categories = {}

        for invoice in request.data['invoice_lines']:
            price = int(invoice['unit_price_net'].replace('.', '')) * invoice['quantity']

            if invoice['category'] in categories:
                categories[invoice['category']] += price

            else:
                categories[invoice['category']] = price

        # Generate bookkeeping data

        payment_data = []

        for count, payment in enumerate(request.data['payments']):
            data = {'id': count + 1, 'categorisations': []}

            total_price = sum(categories.values())
            available = int(payment['amount'].replace('.', ''))

            for price in categories.values():
                distributed_amount = round(price / total_price * available)

                if distributed_amount < price:
                    amount_euros = f'{distributed_amount / 100:.2f}'
                    available -= distributed_amount

                else:
                    amount_euros = f'{price / 100:.2f}'
                    available -= price

                data['categorisations'].append(amount_euros)
                total_price -= price

            payment_data.append(data)

        # Send response

        return Response(payment_data)
