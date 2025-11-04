"""اسکریپت برای خواندن محتوای PDF رزومه"""
import sys
import os

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    os.system(f"{sys.executable} -m pip install pdfplumber")
    import pdfplumber

def read_cv():
    try:
        with pdfplumber.open('my-cv-fa.pdf') as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            
            # Save to file for review
            with open('cv_content.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            
            return text
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    content = read_cv()
    if content:
        print("CV content extracted successfully!")
        print("=" * 50)
        print(content)
        print("=" * 50)
        print("\nContent also saved to cv_content.txt")
    else:
        print("Failed to read PDF")

