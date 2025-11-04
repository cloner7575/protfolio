# راهنمای ترجمه

برای ترجمه کامل دو زبانه بودن سایت، مراحل زیر را دنبال کنید:

## روش 1: بدون نصب gettext (فقط ایجاد فایل‌های ترجمه)

1. ایجاد فایل‌های ترجمه:
```bash
python manage.py makemessages -l fa
python manage.py makemessages -l en
```

2. ویرایش فایل‌های ترجمه:
- فایل `locale/fa/LC_MESSAGES/django.po` را باز کنید
- ترجمه‌های فارسی را اضافه کنید
- فایل `locale/en/LC_MESSAGES/django.po` را نیز بررسی کنید

3. کامپایل ترجمه‌ها (نیاز به gettext):
```bash
python manage.py compilemessages
```

## روش 2: نصب gettext برای Windows

### گزینه A: استفاده از Chocolatey
```bash
choco install gettext
```

### گزینه B: دانلود دستی
1. از این لینک دانلود کنید: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. فایل‌های اجرایی را به PATH اضافه کنید
3. یا فایل `gettext/bin/` را به PATH اضافه کنید

### گزینه C: استفاده از WSL
اگر Windows Subsystem for Linux نصب دارید:
```bash
wsl
sudo apt-get update
sudo apt-get install gettext
```

## نکته مهم:
حتی اگر compilemessages را اجرا نکنید، Django باز هم از فایل‌های .po استفاده می‌کند (اما کمی کندتر).

## ترجمه‌های پیشنهادی برای django.po:

```
msgid "Portfolio"
msgstr "پورتفولیو"

msgid "Home"
msgstr "خانه"

msgid "About"
msgstr "درباره من"

msgid "Projects"
msgstr "پروژه‌ها"

msgid "Skills"
msgstr "مهارت‌ها"

msgid "Experience"
msgstr "تجربه کاری"

msgid "Education"
msgstr "تحصیلات"

msgid "Blog"
msgstr "بلاگ"

msgid "Contact"
msgstr "تماس"

msgid "View Projects"
msgstr "مشاهده پروژه‌ها"

msgid "Contact Me"
msgstr "تماس با من"

msgid "Latest Projects"
msgstr "آخرین پروژه‌ها"

msgid "Latest Blog Posts"
msgstr "آخرین پست‌های بلاگ"

msgid "Read More"
msgstr "بیشتر بخوانید"

msgid "View Details"
msgstr "مشاهده جزئیات"

msgid "Demo"
msgstr "دمو"

msgid "views"
msgstr "بازدید"

msgid "Full-Stack Developer & Creative Problem Solver"
msgstr "توسعه‌دهنده فول‌استک و حل‌کننده خلاقانه مسائل"

msgid "Check out some of my recent work"
msgstr "برخی از کارهای اخیر من را مشاهده کنید"

msgid "Read my latest articles and tutorials"
msgstr "آخرین مقالات و آموزش‌های من را بخوانید"
```

