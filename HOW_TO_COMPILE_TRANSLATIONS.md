# راهنمای کامپایل ترجمه‌ها

بعد از تغییر فایل `locale/fa/LC_MESSAGES/django.po`، باید آن را به فایل `.mo` کامپایل کنید تا تغییرات اعمال شوند.

## روش 1: استفاده از اسکریپت ساده (توصیه می‌شود)

```bash
python compile_now.py
```

## روش 2: استفاده از Django Management Command

```bash
python manage.py compilemessages_custom
```

## روش 3: استفاده از Django Standard Command (اگر gettext نصب باشد)

```bash
python manage.py compilemessages
```

## بعد از کامپایل

1. **سرور را restart کنید** (اگر در حال اجرا است):
   - سرور Django را متوقف کنید (Ctrl+C)
   - دوباره راه‌اندازی کنید: `python manage.py runserver`

2. **صفحه را refresh کنید** (Ctrl+F5 برای hard refresh)

## نکات مهم

- فایل `.mo` باید در همان پوشه `locale/fa/LC_MESSAGES/` ایجاد شود
- اگر فایل `.mo` وجود دارد، باید حذف شود و دوباره کامپایل شود
- بعد از کامپایل، تغییرات فوراً اعمال می‌شوند (اما بهتر است سرور را restart کنید)

## بررسی صحت کامپایل

بعد از کامپایل، فایل `locale/fa/LC_MESSAGES/django.mo` باید ایجاد شود.

