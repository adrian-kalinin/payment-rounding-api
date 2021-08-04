from rest_framework.views import APIView
from rest_framework.response import Response

from .utils.bookkeeping import separate_categories, generate_bookkeeping_data


class PaymentRoundingView(APIView):
    def post(self, request):
        invoice_lines = request.data['invoice_lines']
        categories = separate_categories(invoice_lines)

        payments = request.data['payments']
        bookkeeping_data = generate_bookkeeping_data(payments, categories)

        return Response(bookkeeping_data)
