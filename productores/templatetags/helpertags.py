from django import template
import locale
register = template.Library()

@register.filter(name='clean')
def limpiarSlug(value):
    return value.replace('_', ' ')


@register.filter(name='percentage')
def calculaperct(value1, value2):
    try:
        resultado = (float(value1) / float(value2) * 100)
        return resultado
    except:
        return 0
