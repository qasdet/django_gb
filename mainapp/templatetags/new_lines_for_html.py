from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def new_lines_for_html(value: str):
    return mark_safe(value.replace("\n", "<br>"))
