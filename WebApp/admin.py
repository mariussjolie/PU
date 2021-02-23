"""WebApp Admin Forms"""
from django.contrib import admin

from .models import Estate, Item, Vote


class ItemInline(admin.TabularInline):
    """Inline input for Items"""
    model = Item


class EstateAdmin(admin.ModelAdmin):
    """Form for adding estate"""
    inlines = [
        ItemInline,
    ]


class VoteInline(admin.TabularInline):
    """Inline input for Votes"""
    model = Vote
    # extra = 3


class ItemAdmin(admin.ModelAdmin):
    """Form for adding Item"""
    inlines = [
        VoteInline,
    ]


admin.site.register(Estate, EstateAdmin)
admin.site.register(Vote)
admin.site.register(Item, ItemAdmin)
