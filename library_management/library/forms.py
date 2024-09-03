# library_management/library/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Library, UserProfile

class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']  # Include only fields that exist in UserProfile model

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'location', 'total_seats']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True
        if commit:
            user.save()
        return user

class AdminUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser']

class AdminUserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


















# from django import forms
# from django.contrib.auth.models import User
# from .models import UserProfile
# from .models import Library

# class StudentSignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'first_name', 'last_name', 'email']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['dob', 'hobbies', 'contact_number', 'address', 'geo_location']














