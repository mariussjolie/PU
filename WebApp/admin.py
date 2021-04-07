"""WebApp Admin Forms"""
# pylint: disable=too-few-public-methods
from django.contrib import admin

from .models import Estate, Item, Vote, Comment


class ItemInline(admin.TabularInline):
    """Inline input for Items"""
    model = Item


class EstateAdmin(admin.ModelAdmin):
    """Form for adding estate"""
    list_display = ('title', 'address')
    inlines = [
        ItemInline,
    ]


class VoteInline(admin.TabularInline):
    """Inline input for Votes"""
    model = Vote
    # extra = 3


class ItemAdmin(admin.ModelAdmin):
    """Form for adding Item"""
    list_display = ('description', 'estate')
    inlines = [
        VoteInline,
    ]


class VoteAdmin(admin.ModelAdmin):
    """Form for adding Vote"""
    list_display = ('item', 'user', 'choice', 'importance')


class CommentAdmin(admin.ModelAdmin):
    """Form for adding and editing Comment"""
    list_display = ('comment', 'user')


admin.site.register(Estate, EstateAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)
