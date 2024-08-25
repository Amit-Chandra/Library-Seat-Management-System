# from django.db import models
# from users.models import User

# class Library(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.TextField()
#     admin = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name
    

# libraries/models.py
from django.db import models
from users.models import User

class Library(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Seat(models.Model):
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    library = models.ForeignKey(Library, related_name='seats', on_delete=models.CASCADE)

    def __str__(self):
        return f"Seat {self.number} in {self.library.name}"


