from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    """Умножает значение на аргумент"""
    return float(value) * float(arg)