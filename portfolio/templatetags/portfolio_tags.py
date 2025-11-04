from django import template
from django.urls import resolve, reverse
from django.utils.translation import get_language
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def change_language(context, lang_code):
    """
    Get the URL of the current page in a different language.
    Works with Django's i18n_patterns.
    Usage: {% change_language 'en' %}
    """
    request = context.get('request')
    if not request:
        return '/'
    
    # Get the current resolved URL name
    current_path = request.path_info
    
    # Remove existing language prefix if any
    for lang, _ in settings.LANGUAGES:
        if current_path.startswith(f'/{lang}/'):
            current_path = current_path[len(f'/{lang}'):]
            break
        elif current_path == f'/{lang}':
            current_path = '/'
            break
    
    # Ensure path starts with /
    if not current_path.startswith('/'):
        current_path = '/' + current_path
    
    # Add new language prefix if not default (en)
    default_lang = settings.LANGUAGE_CODE
    if lang_code != default_lang:
        new_path = f'/{lang_code}{current_path}'
    else:
        # For default language, use path without prefix if prefix_default_language=False
        new_path = current_path
    
    return new_path


@register.simple_tag
def get_language_name(code):
    """Get language name from code"""
    languages = {
        'en': 'English',
        'fa': 'فارسی',
    }
    return languages.get(code, code)


@register.filter
def get_localized_field(obj, field_name):
    """
    Get localized field value based on current language.
    Usage: {{ project|get_localized_field:"title" }}
    """
    language = get_language()
    
    # Try get_field_name method first (most reliable)
    method_name = f"get_{field_name}"
    if hasattr(obj, method_name):
        try:
            return getattr(obj, method_name)(language)
        except:
            pass
    
    # Try to get language-specific field
    lang_field = f"{field_name}_{language}"
    if hasattr(obj, lang_field):
        value = getattr(obj, lang_field)
        if value:
            return value
    
    # Fallback to default field (usually _en)
    default_field = f"{field_name}_en"
    if hasattr(obj, default_field):
        value = getattr(obj, default_field)
        if value:
            return value
    
    # Last resort: try base field name
    if hasattr(obj, field_name):
        return getattr(obj, field_name)
    
    return ""


@register.filter
def localize_category(skill_category):
    """
    Localize skill category names.
    """
    from django.utils.translation import gettext_lazy as _
    
    categories = {
        'frontend': _('Frontend'),
        'backend': _('Backend'),
        'database': _('Database'),
        'tools': _('Tools'),
        'other': _('Other'),
    }
    
    return categories.get(skill_category, skill_category)


@register.filter
def category_icon(skill_category):
    """
    Get Bootstrap icon name for skill category.
    """
    icon_map = {
        'frontend': 'code-slash',
        'backend': 'server',
        'database': 'database',
        'tools': 'tools',
        'other': 'gear',
    }
    return icon_map.get(skill_category, 'code-slash')


@register.simple_tag
def get_current_lang():
    """Get current language code"""
    return get_language()
