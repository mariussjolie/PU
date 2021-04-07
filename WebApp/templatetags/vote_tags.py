"""Template tags for Votes"""
from django import template

register = template.Library()


@register.filter
def on_item(query_set, item):
    """Filter queryset by Item"""
    return query_set.filter(item=item)


@register.filter
def by_user(query_set, user):
    """Filter queryset by User"""
    return query_set.filter(user=user)
