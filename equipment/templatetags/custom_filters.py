from django import template

register = template.Library()

@register.filter
def get_value_from_dict(dict_data, key):
    """
    Фильтр для получения значения из словаря по ключу в шаблонах Django.
    """
    if dict_data:
        return dict_data.get(key)
    return None
