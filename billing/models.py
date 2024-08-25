from django.db import models
from users.models import User
from libraries.models import Library

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text='Duration in days')

    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.payment_method})"
