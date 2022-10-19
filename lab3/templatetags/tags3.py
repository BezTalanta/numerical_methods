from django.templatetags.static import register

@register.simple_tag(takes_context=True)
def output_error_rate(context, el_list, real_el):
    last_el = context[el_list][-1]
    return round(abs(real_el - last_el), 5)

@register.simple_tag
def output_simpson(simp_list, index):
    if int(index) % 2 == 0:
        return simp_list[int(index / 2)]
    return ''
