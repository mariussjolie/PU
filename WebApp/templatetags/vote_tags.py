from django import template

register = template.Library()


@register.filter
def on_item(qs, item):
    return qs.filter(item=item)


@register.filter
def by_user(qs, user):
    return qs.filter(user=user)
