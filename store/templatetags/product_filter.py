from django import template

register = template.Library()

@register.filter()
def root(value): # Only one argument.
  """Returns category root slug"""
  val = value.get(level=0)
  return val.slug


@register.filter()
def values(value, arg):
  """Returns attribute values"""
  values = arg.attribute_values.prefetch_related("attribute").filter(attribute=value)
  return values


@register.filter()
def value_list(value):
  """Returns product type attribute values"""
  values = ""
  for val in value.values("value"):
    values += f"{val['value']}, "
  return values