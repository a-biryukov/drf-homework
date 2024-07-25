import re

from rest_framework.serializers import ValidationError


def validate_urls(value):
    """Проверяет наличие ссылок в тексте"""
    reg = re.compile(r'(http[s]?://)((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
    url = reg.search(value)
    if url and 'youtube.com' not in url.group(2):
        raise ValidationError('Нельзя использовать ссылки, кроме youtube.com')
