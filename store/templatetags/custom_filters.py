from django import template

register = template.Library()

@register.filter
def batch(iterable, size):
    """
    Group an iterable into batches of a given size.
    """
    iterable = list(iterable)
    num_batches = (len(iterable) + size - 1) // size
    batches = [iterable[i*size:(i+1)*size] for i in range(num_batches)]
    return batches



@register.filter(name='attr')
def attr(obj, attr_name):
    return getattr(obj, attr_name)