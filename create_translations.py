"""
اسکریپت کمکی برای ایجاد فایل‌های ترجمه بدون نیاز به gettext
این اسکریپت فایل django.po را برای فارسی ایجاد می‌کند.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale' / 'fa' / 'LC_MESSAGES'
LOCALE_DIR.mkdir(parents=True, exist_ok=True)

PO_FILE = LOCALE_DIR / 'django.po'

# ترجمه‌های پیش‌فرض
TRANSLATIONS = {
    'Portfolio': 'پورتفولیو',
    'Home': 'خانه',
    'About': 'درباره من',
    'Projects': 'پروژه‌ها',
    'Skills': 'مهارت‌ها',
    'Experience': 'تجربه کاری',
    'Education': 'تحصیلات',
    'Blog': 'بلاگ',
    'Contact': 'تماس',
    'View Projects': 'مشاهده پروژه‌ها',
    'Contact Me': 'تماس با من',
    'Latest Projects': 'آخرین پروژه‌ها',
    'Check out some of my recent work': 'برخی از کارهای اخیر من را مشاهده کنید',
    'Latest Blog Posts': 'آخرین پست‌های بلاگ',
    'Read my latest articles and tutorials': 'آخرین مقالات و آموزش‌های من را بخوانید',
    'Read More': 'بیشتر بخوانید',
    'View Details': 'مشاهده جزئیات',
    'Demo': 'دمو',
    'Live Demo': 'دمو زنده',
    'View on GitHub': 'مشاهده در GitHub',
    'views': 'بازدید',
    'No projects available yet.': 'هنوز پروژه‌ای موجود نیست.',
    'No blog posts available yet.': 'هنوز پست بلاگی موجود نیست.',
    'View All Projects': 'مشاهده همه پروژه‌ها',
    'View All Posts': 'مشاهده همه پست‌ها',
    'Hi, I am': 'سلام، من',
    'Full-Stack Developer & Creative Problem Solver': 'توسعه‌دهنده فول‌استک و حل‌کننده خلاقانه مسائل',
    'Personal portfolio and blog': 'پورتفولیو و بلاگ شخصی',
    'Created with Django and Bootstrap': 'ساخته شده با Django و Bootstrap',
    'All rights reserved': 'تمام حقوق محفوظ است',
    'Toggle navigation': 'تغییر ناوبری',
    'Close': 'بستن',
    'Scroll to top': 'اسکرول به بالا',
    'GitHub': 'GitHub',
    'LinkedIn': 'LinkedIn',
    'Twitter': 'توییتر',
    'Email': 'ایمیل',
    'About Me': 'درباره من',
    'I am a passionate Full-Stack Developer with expertise in building modern web applications. I love solving complex problems and creating beautiful, functional user experiences.': 'من یک توسعه‌دهنده فول‌استک پرشور با تخصص در ساخت اپلیکیشن‌های وب مدرن هستم. عاشق حل مسائل پیچیده و ایجاد تجربیات کاربری زیبا و کاربردی هستم.',
    'With years of experience in both frontend and backend development, I specialize in creating scalable, maintainable, and performant applications.': 'با سال‌ها تجربه در توسعه فرانت‌اند و بک‌اند، در ساخت اپلیکیشن‌های مقیاس‌پذیر، قابل نگهداری و با عملکرد بالا تخصص دارم.',
    '5+': '5+',
    'Years Experience': 'سال تجربه',
    '50+': '50+',
    'Projects Completed': 'پروژه تکمیل شده',
    'Get In Touch': 'تماس بگیرید',
    'My Projects': 'پروژه‌های من',
    'A collection of my recent work and side projects': 'مجموعه‌ای از کارها و پروژه‌های جانبی اخیر من',
    'Filter by technology...': 'فیلتر بر اساس تکنولوژی...',
    'Featured': 'ویژه',
    'Work Experience': 'تجربه کاری',
    'My professional journey': 'سفر حرفه‌ای من',
    'Current': 'فعلی',
    'Present': 'در حال حاضر',
    'No experience records available yet.': 'هنوز رکورد تجربه‌ای موجود نیست.',
    'Education': 'تحصیلات',
    'My educational background': 'پس‌زمینه تحصیلی من',
    'No education records available yet.': 'هنوز رکورد تحصیلی موجود نیست.',
    'Get In Touch': 'تماس بگیرید',
    'Have a project in mind? Feel free to reach out!': 'پروژه‌ای در ذهن دارید؟ خوشحال می‌شوم با من تماس بگیرید!',
    'Name': 'نام',
    'Subject': 'موضوع',
    'Message': 'پیام',
    'Send Message': 'ارسال پیام',
    'Phone': 'تلفن',
    'Location': 'موقعیت',
    'City, Country': 'شهر، کشور',
    'Project Info': 'اطلاعات پروژه',
    'Created': 'ایجاد شده',
    'Technologies': 'تکنولوژی‌ها',
    'Featured Project': 'پروژه ویژه',
    'Related Projects': 'پروژه‌های مرتبط',
    'Technologies and tools I work with': 'تکنولوژی‌ها و ابزارهایی که با آنها کار می‌کنم',
    'Frontend': 'فرانت‌اند',
    'Backend': 'بک‌اند',
    'Database': 'دیتابیس',
    'Tools': 'ابزارها',
    'Other': 'سایر',
    'Blog': 'بلاگ',
    'Latest articles and tutorials': 'آخرین مقالات و آموزش‌ها',
    'Search posts...': 'جستجوی پست‌ها...',
    'All': 'همه',
    'Category': 'دسته‌بندی',
    'Back to Blog': 'بازگشت به بلاگ',
    'Published on': 'منتشر شده در',
    'Previous': 'قبلی',
    'Next': 'بعدی',
    'No posts found in this category.': 'پستی در این دسته‌بندی پیدا نشد.',
}

# Header فایل PO
PO_HEADER = '''# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: Django Portfolio\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-01-01 12:00+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: fa\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n==0 || n==1);\\n"

'''

def create_po_file():
    """ایجاد فایل django.po با ترجمه‌های پیش‌فرض"""
    content = PO_HEADER
    
    for msgid, msgstr in sorted(TRANSLATIONS.items()):
        content += f'\nmsgid "{msgid}"\n'
        content += f'msgstr "{msgstr}"\n'
    
    with open(PO_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'File created: {PO_FILE}')
    print(f'Number of translations: {len(TRANSLATIONS)}')
    print('\nTo compile translations, install gettext and run:')
    print('python manage.py compilemessages')

if __name__ == '__main__':
    create_po_file()

