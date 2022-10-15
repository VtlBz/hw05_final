# core/templatetags/user_filters.py

from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def is_current_page(request, param):
    return request == param
