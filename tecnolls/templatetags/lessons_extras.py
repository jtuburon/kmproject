from django import template
register = template.Library()

@register.simple_tag
def tagslabels(lesson):
    return ",".join([s.label for s in lesson.tags])