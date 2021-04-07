"""WebApp Forms"""
# pylint: disable=too-few-public-methods
from django import forms
from django.contrib.auth.models import User

from .models import Item, Vote, Comment


class ItemForm(forms.ModelForm):
    """Form for adding Item"""

    class Meta:
        """Meta class under ItemForm"""
        model = Item
        fields = ['estate', 'description', 'picture']


VOTE_CHOICES = (
    ("throw", "Throw"),
    ("keep", "Keep"),
    ("donate", "Donate"),
)

VOTE_IMPORTANCE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
)


class VoteForm(forms.ModelForm):
    """Form for adding user choice and importance"""
    choice = forms.ChoiceField(choices=VOTE_CHOICES)
    importance = forms.ChoiceField(choices=VOTE_IMPORTANCE)

    class Meta:
        """Meta class for VoteForm"""
        model = Vote
        fields = ('choice', 'importance')


class DistributeItemForm(forms.ModelForm):
    """Form for distributing items"""
    owner = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        """Meta class for DistributeItemForm"""
        model = Item
        fields = ['owner']


class CommentForm(forms.ModelForm):
    """Form for adding comment"""
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        """Meta class for CommentForm"""
        model = Comment
        fields = ('comment',)
