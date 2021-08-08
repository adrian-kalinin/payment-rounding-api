from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import HttpResponseNotFound

import json

from .utils.bookkeeping import separate_categories, generate_bookkeeping_data, prepare_payment_data
from .serializers import InvoiceLinesAndPaymentsSerializer


def page_not_found(*args, **argv):
    response_data = json.dumps({'message': 'Page not found'})
    return HttpResponseNotFound(response_data, content_type='application/json')


class PaymentRoundingView(APIView):
    def post(self, request):
        serializer = InvoiceLinesAndPaymentsSerializer(data=request.data)

        if serializer.is_valid():
            invoice_lines = request.data['invoice_lines']
            categories = separate_categories(invoice_lines)

            raw_payments = request.data['payments']
            prepared_payments = prepare_payment_data(raw_payments)
            bookkeeping_data = generate_bookkeeping_data(prepared_payments, categories)

            return Response(bookkeeping_data)

        else:
            response_data = {'message': 'Invalid request body'}
            return Response(response_data, status=HTTP_400_BAD_REQUEST)
