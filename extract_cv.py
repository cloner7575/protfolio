#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract text from CV PDF"""
import sys

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber

def extract_cv():
    pdf_path = 'my-cv-fa.pdf'
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    all_text.append(f"=== PAGE {i+1} ===\n{text}\n")
            
            full_text = '\n'.join(all_text)
            
            # Save to file
            with open('cv_content.txt', 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            print("SUCCESS: CV content extracted and saved to cv_content.txt")
            print("\n" + "="*60)
            print("EXTRACTED CONTENT:")
            print("="*60)
            print(full_text)
            print("="*60)
            return full_text
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    extract_cv()

