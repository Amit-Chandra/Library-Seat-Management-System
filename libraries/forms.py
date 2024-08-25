from django import forms
from .models import Library

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'address']
