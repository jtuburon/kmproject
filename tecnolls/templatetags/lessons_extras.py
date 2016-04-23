from django import template
register = template.Library()

@register.simple_tag
def tagslabels(lesson):
    return ",".join([s.label for s in lesson.tags])

@register.simple_tag
def resulttagslabels(lesson):
    return [s["label"].encode('UTF8') for s in lesson.tags]