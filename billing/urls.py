# billing/urls.py
from django.urls import path
from .views import record_payment, payment_success

urlpatterns = [
    path('record/', record_payment, name='record_payment'),
    path('success/', payment_success, name='payment_success'),
]
