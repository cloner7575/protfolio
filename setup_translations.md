# راهنمای نصب و استفاده از ترجمه‌ها

## مشکل: Can't find msgfmt

این خطا به این معنی است که ابزارهای GNU gettext روی سیستم شما نصب نیستند.

## راه‌حل‌ها:

### راه‌حل 1: نصب gettext با Chocolatey (پیشنهادی برای Windows)

اگر Chocolatey نصب دارید:
```powershell
choco install gettext
```

اگر Chocolatey ندارید، ابتدا نصب کنید:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### راه‌حل 2: دانلود مستقیم gettext

1. از این لینک دانلود کنید: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. فایل ZIP را استخراج کنید
3. مسیر `gettext/bin/` را به PATH محیطی اضافه کنید:
   - System Properties > Environment Variables
   - PATH را ویرایش کنید
   - مسیر `C:\path\to\gettext\bin` را اضافه کنید

### راه‌حل 3: استفاده از WSL (Windows Subsystem for Linux)

```bash
wsl
sudo apt-get update
sudo apt-get install gettext
```

سپس در WSL دستورات Django را اجرا کنید.

### راه‌حل 4: بدون کامپایل (فقط برای تست)

حتی بدون gettext می‌توانید فایل‌های ترجمه را ایجاد کنید، اما باید:
1. فایل‌های `.po` را به صورت دستی ویرایش کنید
2. از پکیج‌های Python برای کامپایل استفاده کنید

```bash
pip install python-gettext
```

### راه‌حل 5: استفاده از Django بدون کامپایل

Django می‌تواند فایل‌های `.po` را به صورت مستقیم بخواند (کندتر اما کار می‌کند):

```bash
# ایجاد فایل‌های ترجمه
python manage.py makemessages -l fa
python manage.py makemessages -l en
```

سپس فایل‌های `locale/fa/LC_MESSAGES/django.po` را ویرایش کنید.

## مراحل کامل ترجمه:

1. **فعال کردن virtual environment** (اگر دارید):
```bash
venv\Scripts\activate
# یا
env\Scripts\activate
```

2. **ایجاد فایل‌های ترجمه**:
```bash
python manage.py makemessages -l fa
python manage.py makemessages -l en
```

3. **ویرایش فایل‌های ترجمه**:
- باز کردن `locale/fa/LC_MESSAGES/django.po`
- ترجمه‌های فارسی را اضافه کنید

4. **کامپایل ترجمه‌ها** (بعد از نصب gettext):
```bash
python manage.py compilemessages
```

## مثال ترجمه در django.po:

```po
msgid "Portfolio"
msgstr "پورتفولیو"

msgid "Home"
msgstr "خانه"

msgid "About"
msgstr "درباره من"

msgid "Projects"
msgstr "پروژه‌ها"

msgid "View Projects"
msgstr "مشاهده پروژه‌ها"

msgid "Contact Me"
msgstr "تماس با من"

msgid "Latest Projects"
msgstr "آخرین پروژه‌ها"

msgid "Full-Stack Developer & Creative Problem Solver"
msgstr "توسعه‌دهنده فول‌استک و حل‌کننده خلاقانه مسائل"

msgid "Check out some of my recent work"
msgstr "برخی از کارهای اخیر من را مشاهده کنید"

msgid "Read More"
msgstr "بیشتر بخوانید"

msgid "View Details"
msgstr "مشاهده جزئیات"

msgid "Demo"
msgstr "دمو"

msgid "views"
msgstr "بازدید"

msgid "No projects available yet."
msgstr "هنوز پروژه‌ای موجود نیست."

msgid "No blog posts available yet."
msgstr "هنوز پست بلاگی موجود نیست."
```

## نکته مهم:

حتی اگر `compilemessages` را اجرا نکنید، Django باز هم می‌تواند از فایل‌های `.po` استفاده کند (اما کمی کندتر). فقط مطمئن شوید که فایل‌های `.po` درست ویرایش شده‌اند.

