from django.contrib.auth.models import AbstractUser
from django.db import models
from libraries.models import Library

class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='admins')

    def has_access_to_library(self, library):
        if self.role == 'super_admin':
            return True
        if self.role == 'admin' and self.library == library:
            return True
        return False
