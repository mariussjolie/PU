from django.contrib import admin

from .models import Estate, Item


class ItemInline(admin.TabularInline):
    model = Item


class EstateAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]


admin.site.register(Estate, EstateAdmin)
admin.site.register(Item)
