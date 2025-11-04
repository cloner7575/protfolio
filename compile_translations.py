"""
اسکریپت جایگزین برای کامپایل ترجمه‌ها بدون نیاز به msgfmt
این اسکریپت فایل‌های .po را به .mo تبدیل می‌کند.
"""

import os
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'


def unescape_string(s):
    """Unescape PO file strings"""
    if not s:
        return s
    s = s.replace('\\"', '"')
    s = s.replace('\\n', '\n')
    s = s.replace('\\t', '\t')
    s = s.replace('\\\\', '\\')
    return s


def parse_po_file(po_path):
    """Parse a .po file and return list of (msgid, msgstr) tuples"""
    entries = []
    
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    current_msgid = []
    current_msgstr = []
    in_msgid = False
    in_msgstr = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Start of msgid
        if stripped.startswith('msgid '):
            # Save previous entry
            if current_msgid and current_msgstr:
                msgid_str = unescape_string(''.join(current_msgid))
                msgstr_str = unescape_string(''.join(current_msgstr))
                if msgid_str:  # Skip header (empty msgid)
                    entries.append((msgid_str, msgstr_str))
            
            # Start new entry
            current_msgid = []
            current_msgstr = []
            
            # Extract first part of msgid
            rest = stripped[6:].strip()  # After "msgid "
            if rest.startswith('"') and rest.endswith('"'):
                current_msgid.append(rest[1:-1])
            elif rest.startswith('"'):
                current_msgid.append(rest[1:])
            elif rest:
                current_msgid.append(rest)
            
            in_msgid = True
            in_msgstr = False
            
        # Start of msgstr
        elif stripped.startswith('msgstr '):
            # Extract first part of msgstr
            rest = stripped[7:].strip()  # After "msgstr "
            if rest.startswith('"') and rest.endswith('"'):
                current_msgstr.append(rest[1:-1])
            elif rest.startswith('"'):
                current_msgstr.append(rest[1:])
            elif rest:
                current_msgstr.append(rest)
            
            in_msgid = False
            in_msgstr = True
        
        # Continuation line (multiline string)
        elif stripped.startswith('"') and stripped.endswith('"'):
            content = stripped[1:-1]
            if in_msgid:
                current_msgid.append(content)
            elif in_msgstr:
                current_msgstr.append(content)
        
        # Empty line or end of entry
        elif not stripped:
            if current_msgid and current_msgstr:
                msgid_str = unescape_string(''.join(current_msgid))
                msgstr_str = unescape_string(''.join(current_msgstr))
                if msgid_str:  # Skip header
                    entries.append((msgid_str, msgstr_str))
                current_msgid = []
                current_msgstr = []
                in_msgid = False
                in_msgstr = False
        
        i += 1
    
    # Add last entry if exists
    if current_msgid and current_msgstr:
        msgid_str = unescape_string(''.join(current_msgid))
        msgstr_str = unescape_string(''.join(current_msgstr))
        if msgid_str:  # Skip header
            entries.append((msgid_str, msgstr_str))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_entries = []
    for msgid, msgstr in entries:
        if isinstance(msgid, str) and isinstance(msgstr, str):
            if msgid not in seen:
                seen.add(msgid)
                unique_entries.append((msgid, msgstr))
    
    return unique_entries


def create_mo_file(entries, mo_path):
    """Create a .mo file from entries (GNU gettext binary format)
    
    MO file format (correct structure):
    - Header (28 bytes)
    - Original strings table: pairs of (length, offset)
    - Translated strings table: pairs of (length, offset)
    - String pairs: each pair is msgid + null + msgstr + null (stored together)
    
    Important: All strings must be UTF-8 encoded.
    """
    # Filter out empty msgid (header)
    entries = [(msgid, msgstr) for msgid, msgstr in entries 
               if msgid and isinstance(msgid, str) and isinstance(msgstr, str)]
    
    if not entries:
        print(f"  -> No valid entries found")
        return
    
    # Sort entries for binary search
    entries_sorted = sorted(entries, key=lambda x: x[0])
    num_strings = len(entries_sorted)
    
    # First pass: build string pairs to calculate exact sizes
    string_pairs = []
    for msgid, msgstr in entries_sorted:
        try:
            # Encode strings as UTF-8
            msgid_bytes = msgid.encode('utf-8')
            msgstr_bytes = msgstr.encode('utf-8')
        except (UnicodeEncodeError, AttributeError) as e:
            print(f"  Warning: Skipping entry due to encoding error: {e}")
            continue
        
        # Create the pair: msgid + null + msgstr + null
        pair_data = msgid_bytes + b'\x00' + msgstr_bytes + b'\x00'
        
        # Calculate offsets
        msgid_length = len(msgid_bytes) + 1  # including null
        msgstr_length = len(msgstr_bytes) + 1  # including null
        
        string_pairs.append({
            'data': pair_data,
            'msgid_length': msgid_length,
            'msgstr_length': msgstr_length,
            'pair_length': len(pair_data),
        })
    
    if not string_pairs:
        print(f"  -> No valid string pairs to write")
        return
    
    # Update num_strings
    num_strings = len(string_pairs)
    
    # Calculate offsets
    header_size = 28
    original_table_size = num_strings * 8  # 4 bytes length + 4 bytes offset per entry
    translated_table_size = num_strings * 8
    original_table_offset = header_size
    translated_table_offset = original_table_offset + original_table_size
    strings_offset = translated_table_offset + translated_table_size
    
    # Second pass: calculate actual offsets for each pair
    current_offset = strings_offset
    for pair in string_pairs:
        msgid_bytes_len = pair['msgid_length'] - 1  # without null
        pair['msgid_offset'] = current_offset
        pair['msgstr_offset'] = current_offset + msgid_bytes_len + 1
        current_offset += pair['pair_length']
    
    # Write MO file in binary mode
    with open(mo_path, 'wb') as f:
        # Write header (7 * 4 bytes = 28 bytes)
        f.write(struct.pack('<I', 0x950412de))  # Magic number (little endian)
        f.write(struct.pack('<I', 0))  # File format revision
        f.write(struct.pack('<I', num_strings))  # Number of strings
        f.write(struct.pack('<I', original_table_offset))  # Offset of table with original strings
        f.write(struct.pack('<I', translated_table_offset))  # Offset of table with translation strings
        f.write(struct.pack('<I', 0))  # Size of hash table (we skip it)
        f.write(struct.pack('<I', 0))  # Offset of hash table
        
        # Write original strings table (length, offset pairs)
        for pair in string_pairs:
            f.write(struct.pack('<I', pair['msgid_length']))
            f.write(struct.pack('<I', pair['msgid_offset']))
        
        # Write translated strings table (length, offset pairs)
        for pair in string_pairs:
            f.write(struct.pack('<I', pair['msgstr_length']))
            f.write(struct.pack('<I', pair['msgstr_offset']))
        
        # Write string pairs (msgid + null + msgstr + null for each entry)
        for pair in string_pairs:
            f.write(pair['data'])


def compile_translations():
    """Compile all .po files to .mo files"""
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
                    print(f"Compiling {po_file}...")
                    entries = parse_po_file(po_file)
                    if entries:
                        create_mo_file(entries, mo_file)
                        print(f"  -> Created {mo_file} ({len(entries)} translations)")
                        compiled += 1
                    else:
                        print(f"  -> No entries found in {po_file}")
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
    compile_translations()
