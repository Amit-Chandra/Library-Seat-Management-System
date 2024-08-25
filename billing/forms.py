# billing/forms.py
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'library', 'plan', 'amount', 'payment_method']
