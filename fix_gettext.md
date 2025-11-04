# راهنمای حل مشکل gettext در Windows

## مشکل: Can't find msgfmt

اگر بعد از نصب gettext هنوز این خطا را می‌بینید، به این معنی است که:
1. gettext در PATH محیطی شما نیست
2. یا نیاز به راه‌اندازی مجدد terminal/PowerShell دارید

## راه‌حل‌های پیشنهادی:

### راه‌حل 1: استفاده از اسکریپت جایگزین (ساده‌ترین)

ما یک اسکریپت Python ایجاد کرده‌ایم که بدون نیاز به msgfmt کار می‌کند:

```bash
python compile_translations.py
```

یا:

```bash
python manage.py compilemessages_custom
```

این دستورات فایل‌های `.po` را به `.mo` تبدیل می‌کنند.

### راه‌حل 2: افزودن gettext به PATH

اگر gettext را با Chocolatey نصب کرده‌اید:

```powershell
# پیدا کردن محل نصب
$gettextPath = (Get-Command msgfmt -ErrorAction SilentlyContinue).Source
if ($gettextPath) {
    $gettextDir = Split-Path $gettextPath
    Write-Host "Found gettext at: $gettextDir"
} else {
    # معمولاً در یکی از این مسیرهاست:
    $possiblePaths = @(
        "C:\Program Files\gettext\bin",
        "C:\Program Files (x86)\gettext\bin",
        "$env:ProgramFiles\gettext\bin",
        "$env:LOCALAPPDATA\gettext\bin"
    )
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            Write-Host "Found gettext at: $path"
            break
        }
    }
}
```

سپس به صورت موقت در PowerShell:

```powershell
$env:PATH += ";C:\path\to\gettext\bin"
python manage.py compilemessages
```

یا به صورت دائمی:
1. System Properties > Environment Variables
2. PATH را ویرایش کنید
3. مسیر `C:\path\to\gettext\bin` را اضافه کنید
4. PowerShell را بسته و دوباره باز کنید

### راه‌حل 3: استفاده از WSL

اگر Windows Subsystem for Linux دارید:

```bash
wsl
sudo apt-get update
sudo apt-get install gettext
python manage.py compilemessages
```

### راه‌حل 4: دانلود مستقیم gettext

1. از این لینک دانلود کنید: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. فایل ZIP را استخراج کنید
3. مسیر `gettext/bin/` را به PATH اضافه کنید

## استفاده از اسکریپت جایگزین (توصیه می‌شود)

ما یک management command ایجاد کرده‌ایم که می‌توانید استفاده کنید:

```bash
python manage.py compilemessages_custom
```

این دستور بدون نیاز به gettext کار می‌کند و فایل‌های `.mo` را ایجاد می‌کند.

## تست ترجمه‌ها

بعد از کامپایل:

1. سرور را اجرا کنید:
```bash
python manage.py runserver
```

2. به آدرس فارسی بروید:
- http://127.0.0.1:8000/fa/
- یا http://127.0.0.1:8000/fa/about/

3. همه متن‌ها باید به فارسی نمایش داده شوند.

## اگر ترجمه‌ها کار نکرد:

1. مطمئن شوید که فایل `.mo` ایجاد شده است
2. سرور را restart کنید
3. کش مرورگر را پاک کنید
4. مطمئن شوید که `LOCALE_PATHS` در `settings.py` درست تنظیم شده است

