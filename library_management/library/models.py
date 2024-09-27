from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)  # Keeps location information
    total_seats = models.PositiveIntegerField(default=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


# ========================= Seat Model ============================
class Seat(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveIntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} in {self.library.name}"

# ========================= User Profile with Geo-location ============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('superadmin', 'Super Admin'), ('admin', 'Admin'), ('student', 'Student')))
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    dob = models.DateField(null=True, blank=True)
    hobbies = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)

    # Add latitude and longitude to store user's geo-location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    approved = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

# ========================= Payment Model ============================
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.username}"
















# ========================= Library Model with Latitude and Longitude ============================
# class Library(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=255)
#     total_seats = models.PositiveIntegerField()
#     address = models.CharField(max_length=255, blank=True)
#     # owner = models.ForeignKey(User, on_delete=models.CASCADE) 
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

#     # Add latitude and longitude fields to store geo-location
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

#     def __str__(self):
#         return self.name








# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class Library(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=255)
#     total_seats = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name

# class Seat(models.Model):
#     library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='seats')
#     seat_number = models.PositiveIntegerField()
#     is_occupied = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Seat {self.seat_number} in {self.library.name}"

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=(('superadmin', 'Super Admin'), ('admin', 'Admin'), ('student', 'Student')))
#     library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     hobbies = models.TextField(blank=True)
#     contact_number = models.CharField(max_length=15, blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     geo_location = models.CharField(max_length=255, blank=True)
#     approved = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

# class Payment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(default=timezone.now)
#     is_confirmed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Payment of {self.amount} by {self.student.username}"



























# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class Library(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=255)
#     total_seats = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name

# class Seat(models.Model):
#     library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='seats')
#     seat_number = models.PositiveIntegerField()
#     is_occupied = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Seat {self.seat_number} in {self.library.name}"

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=(('superadmin', 'Super Admin'), ('admin', 'Admin'), ('student', 'Student')))
#     library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     hobbies = models.TextField(blank=True)
#     contact_number = models.CharField(max_length=15, blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     geo_location = models.CharField(max_length=255, blank=True)
#     approved = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

# class Payment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(default=timezone.now)
#     is_confirmed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Payment of {self.amount} by {self.student.username}"
    




