from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'hobbies', 'contact_number', 'address', 'geo_location']
