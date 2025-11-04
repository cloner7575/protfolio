"""
اسکریپت جایگزین برای کامپایل ترجمه‌ها با استفاده از polib
این روش مطمئن‌تر است چون از یک کتابخانه استاندارد استفاده می‌کند.
"""

try:
    import polib
    POLIB_AVAILABLE = True
except ImportError:
    POLIB_AVAILABLE = False
    print("polib not installed. Install with: pip install polib")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'


def compile_translations_polib():
    """Compile all .po files to .mo files using polib"""
    if not POLIB_AVAILABLE:
        print("polib is not available. Please install it first: pip install polib")
        return
    
    if not LOCALE_DIR.exists():
        print(f"Locale directory not found: {LOCALE_DIR}")
        return
    
    compiled = 0
    for lang_dir in LOCALE_DIR.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
            mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
            
            if po_file.exists():
                try:
                    print(f"Compiling {po_file} with polib...")
                    po = polib.pofile(str(po_file))
                    po.save_as_mofile(str(mo_file))
                    print(f"  -> Created {mo_file} ({len(po)} translations)")
                    compiled += 1
                except Exception as e:
                    print(f"  Error compiling {po_file}: {e}")
                    import traceback
                    traceback.print_exc()
    
    if compiled > 0:
        print(f"\nSuccessfully compiled {compiled} translation file(s)!")
        print("You can now use translations in your Django project.")
    else:
        print("\nNo translation files found to compile.")


if __name__ == '__main__':
    compile_translations_polib()

