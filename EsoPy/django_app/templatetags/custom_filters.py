# custom_filters.py

from django import template
import re

register = template.Library()

@register.filter(name='remove_suffix')
def remove_suffix(value):
    return value.split('^')[0].strip()

@register.filter(name='extract_numbers')
def extract_numbers(value):
    value = value.replace('|cffffff', '')
    value = value.replace('|r', '')
    value = value.replace('\\r\\n\\r\\n', '\n')
    
    return value