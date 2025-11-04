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


@register.filter
def jalali_date(date_obj, format_string='%Y/%m/%d'):
    """
    Convert a date/datetime object to Jalali (Persian) date format.
    Usage: {{ experience.start_date|jalali_date:"%Y/%m" }}
    
    Available format codes:
    %Y: 4-digit year (e.g., 1403)
    %y: 2-digit year (e.g., 03)
    %m: Month number (01-12)
    %B: Month name (فروردین, اردیبهشت, ...)
    %b: Short month name (فرر, ارد, ...)
    %d: Day of month (01-31)
    %A: Weekday name (شنبه, یکشنبه, ...)
    %a: Short weekday name (ش, ی, ...)
    """
    if not date_obj:
        return ''
    
    try:
        import jdatetime
        from django.utils.translation import get_language
        
        # Convert date to jdatetime
        if hasattr(date_obj, 'year'):  # datetime or date object
            jalali_dt = jdatetime.datetime.fromgregorian(
                year=date_obj.year,
                month=date_obj.month,
                day=date_obj.day
            )
        else:
            return str(date_obj)
        
        # Format the date
        formatted = jalali_dt.strftime(format_string)
        
        # If language is Persian, translate month names
        language = get_language()
        if language == 'fa':
            # Persian month names
            month_names = {
                'Farvardin': 'فروردین',
                'Ordibehesht': 'اردیبهشت',
                'Khordad': 'خرداد',
                'Tir': 'تیر',
                'Mordad': 'مرداد',
                'Shahrivar': 'شهریور',
                'Mehr': 'مهر',
                'Aban': 'آبان',
                'Azar': 'آذر',
                'Dey': 'دی',
                'Bahman': 'بهمن',
                'Esfand': 'اسفند',
            }
            
            # Replace English month names with Persian
            for en_name, fa_name in month_names.items():
                formatted = formatted.replace(en_name, fa_name)
        
        return formatted
    except ImportError:
        # Fallback to regular date formatting if jdatetime is not available
        return date_obj.strftime(format_string) if hasattr(date_obj, 'strftime') else str(date_obj)
    except Exception:
        return str(date_obj)
