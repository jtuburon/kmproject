from django import template
register = template.Library()

@register.simple_tag
def tagslabels(lesson):
    return ",".join([s.label for s in lesson.tags])

@register.simple_tag
def fullname(user):
    return " ".join([user.first_name, user.last_name])