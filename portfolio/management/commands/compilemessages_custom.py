"""
Management command برای کامپایل ترجمه‌ها بدون نیاز به msgfmt
استفاده: python manage.py compilemessages_custom

این command از polib استفاده می‌کند که یک جایگزین Python خالص برای msgfmt است.
"""

try:
    import polib
    POLIB_AVAILABLE = True
except ImportError:
    POLIB_AVAILABLE = False

from django.core.management.base import BaseCommand
import os
from pathlib import Path
from django.conf import settings


# Note: The old manual MO file creation code has been replaced with polib
# which is more reliable and handles encoding correctly.


class Command(BaseCommand):
    help = 'Compile translation files to .mo format without needing msgfmt (uses polib)'

    def handle(self, *args, **options):
        if not POLIB_AVAILABLE:
            self.stdout.write(
                self.style.ERROR(
                    'polib is not installed. Please install it with: pip install polib'
                )
            )
            return
        
        locale_dirs = []
        
        # Add LOCALE_PATHS from settings
        if hasattr(settings, 'LOCALE_PATHS'):
            locale_dirs.extend(settings.LOCALE_PATHS)
        
        compiled = 0
        # Find all locale directories
        for locale_dir in locale_dirs:
            if os.path.exists(locale_dir):
                for lang_dir in Path(locale_dir).iterdir():
                    if lang_dir.is_dir():
                        po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
                        mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
                        
                        if po_file.exists():
                            try:
                                self.stdout.write(f'Processing {po_file}...')
                                po = polib.pofile(str(po_file))
                                po.save_as_mofile(str(mo_file))
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  -> Compiled {mo_file} ({len(po)} translations)'
                                    )
                                )
                                compiled += 1
                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(f'  Error: {e}')
                                )
        
        if compiled > 0:
            self.stdout.write(self.style.SUCCESS(f'\nCompilation complete! Compiled {compiled} file(s).'))
        else:
            self.stdout.write(self.style.WARNING('\nNo translation files found to compile.'))

