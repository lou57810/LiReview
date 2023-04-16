from django import template

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_ticket_display(context, user):
    if context['user'] == user:
        return 'Vous'
    return user


@register.simple_tag(takes_context=True)
def get_review_id(context, id):
    if context['id'] == id:
        return 'True'
    return 'False'


@register.simple_tag(takes_context=True)
def get_review_display(context, user):
    if context['user'] == user:
        return 'Vous'
    return user
