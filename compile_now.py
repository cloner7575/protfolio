#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick compile script"""
import sys
import os

try:
    import polib
except ImportError:
    print("Installing polib...")
    os.system(f"{sys.executable} -m pip install polib -q")
    import polib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'

if LOCALE_DIR.exists():
    for lang_dir in LOCALE_DIR.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
            mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
            
            if po_file.exists():
                try:
                    print(f"Compiling {po_file}...")
                    po = polib.pofile(str(po_file))
                    po.save_as_mofile(str(mo_file))
                    print(f"  -> Created {mo_file} ({len(po)} translations)")
                except Exception as e:
                    print(f"  Error: {e}")
    print("\n✅ Compilation complete!")
else:
    print(f"Locale directory not found: {LOCALE_DIR}")

