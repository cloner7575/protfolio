from django.utils.translation import get_language


def language_context(request):
    """
    Add current language to template context.
    This makes LANGUAGE_CODE available in all templates.
    """
    return {
        'CURRENT_LANGUAGE': get_language(),
    }

