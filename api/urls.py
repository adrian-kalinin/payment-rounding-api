from django.urls import path

from .views import PaymentRoundingView


app_name = 'api'

urlpatterns = [
    path('', PaymentRoundingView.as_view(), name='payment-rounding')
]
