"""WebApp Forms"""
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
        model = Vote
        fields = ('choice', 'importance')


class DistributeItemForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False))

    class Meta:
        model = Item
        fields = ['owner']

class CommentForm(forms.ModelForm):
    """Form for adding comment"""
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment',)
