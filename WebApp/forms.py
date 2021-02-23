"""WebApp Forms"""
from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    """Form for adding Item"""
    class Meta:
        """Meta class under ItemForm"""
        model = Item
        fields = ['estate', 'description', 'picture']
