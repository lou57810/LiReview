from django import template

register = template.Library()

@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_ticket_display(context, user):
    if context['user'] == user:
        return ''
    return user


@register.simple_tag(takes_context=True)
def get_review_display(context, user):
    if context['user'] == user:
        return 'Vous'
    return user