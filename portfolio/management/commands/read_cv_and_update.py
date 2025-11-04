"""Management command برای خواندن رزومه PDF و به‌روزرسانی محتوای سایت"""
from django.core.management.base import BaseCommand
import sys
import os

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

from portfolio.models import Skill, Experience, Education, Project
from django.contrib.auth.models import User
from datetime import date


class Command(BaseCommand):
    help = 'Read CV PDF and update portfolio content'

    def add_arguments(self, parser):
        parser.add_argument('--pdf-path', type=str, default='my-cv-fa.pdf',
                          help='Path to CV PDF file')

    def handle(self, *args, **options):
        pdf_path = options['pdf_path']
        
        if not PDFPLUMBER_AVAILABLE:
            self.stdout.write(self.style.ERROR('pdfplumber is not installed.'))
            self.stdout.write(self.style.WARNING('Installing pdfplumber...'))
            os.system(f"{sys.executable} -m pip install pdfplumber")
            try:
                import pdfplumber
            except ImportError:
                self.stdout.write(self.style.ERROR('Failed to install pdfplumber'))
                return
        
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'PDF file not found: {pdf_path}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Reading CV from: {pdf_path}'))
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ''
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
            
            # Save extracted text for review
            with open('cv_content.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            
            self.stdout.write(self.style.SUCCESS('CV content extracted successfully!'))
            self.stdout.write(self.style.SUCCESS('Content saved to cv_content.txt'))
            self.stdout.write('\n' + '='*50)
            self.stdout.write('EXTRACTED CONTENT:')
            self.stdout.write('='*50)
            self.stdout.write(text)
            self.stdout.write('='*50)
            self.stdout.write('\nPlease review the content and I will update the portfolio data.')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading PDF: {e}'))
            import traceback
            traceback.print_exc()

