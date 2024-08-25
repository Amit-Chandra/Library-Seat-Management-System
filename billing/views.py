# billing/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, Payment
from .forms import PaymentForm

@login_required
def record_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()
    return render(request, 'billing/record_payment.html', {'form': form})

def payment_success(request):
    return render(request, 'billing/payment_success.html')
