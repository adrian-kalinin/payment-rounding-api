from rest_framework import serializers


class InvoiceLineSerializer(serializers.Serializer):
    description = serializers.CharField()
    quantity = serializers.IntegerField()
    category = serializers.CharField()
    unit_price_net = serializers.CharField()


class PaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.CharField()


class InvoiceLinesAndPaymentsSerializer(serializers.Serializer):
    invoice_lines = InvoiceLineSerializer(many=True)
    payments = PaymentSerializer(many=True)
