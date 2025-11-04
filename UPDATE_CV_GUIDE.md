# راهنمای به‌روزرسانی سایت با رزومه

## نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

یا فقط pdfplumber:

```bash
pip install pdfplumber
```

## استفاده از Command

### 1. استخراج محتوا از PDF (بدون به‌روزرسانی دیتابیس)

```bash
python manage.py update_from_cv --extract-only
```

این دستور فقط محتوای PDF را استخراج می‌کند و در فایل `cv_content.txt` ذخیره می‌کند. می‌توانید این فایل را بررسی کنید.

### 2. به‌روزرسانی کامل سایت

```bash
python manage.py update_from_cv
```

این دستور:
- PDF را می‌خواند
- مهارت‌ها، تجربیات، تحصیلات و پروژه‌ها را استخراج می‌کند
- آنها را در دیتابیس ذخیره می‌کند (به صورت دو زبانه)

### 3. پاک کردن داده‌های قبلی و به‌روزرسانی

```bash
python manage.py update_from_cv --clear-existing
```

این دستور داده‌های قبلی را پاک می‌کند و سپس داده‌های جدید را اضافه می‌کند.

## نکات مهم

### 1. ترجمه‌های فارسی

Parser به صورت خودکار ترجمه‌های فارسی را نمی‌سازد. پس از اجرای command:

1. به Django Admin بروید (`/admin/`)
2. برای هر Experience، Education و Project:
   - فیلدهای `title_fa` و `description_fa` را به فارسی پر کنید
   - یا اگر رزومه شما فارسی است، فیلدهای `_en` را به انگلیسی پر کنید

### 2. مهارت‌ها

Parser به صورت خودکار مهارت‌های رایج را شناسایی می‌کند:
- Python, Django, JavaScript, React, HTML/CSS
- PostgreSQL, MySQL, MongoDB
- Git, Docker, Linux
- و غیره...

می‌توانید مهارت‌های بیشتر را در Django Admin اضافه کنید.

### 3. تجربیات کاری

Parser سعی می‌کند تجربیات را از تاریخ‌ها و نام شرکت‌ها استخراج کند، اما ممکن است نیاز به تنظیم دستی داشته باشد.

### 4. تحصیلات

Parser سعی می‌کند مدارک تحصیلی را شناسایی کند. تاریخ‌ها ممکن است نیاز به تنظیم دستی داشته باشند.

### 5. پروژه‌ها

Parser پروژه‌ها را از کلمات کلیدی مانند "project"، "app"، "website" شناسایی می‌کند.

## بهبود Parser

اگر parser به درستی کار نمی‌کند، می‌توانید:

1. فایل `cv_content.txt` را بررسی کنید
2. فایل `portfolio/management/commands/update_from_cv.py` را باز کنید
3. توابع `_parse_experiences`, `_parse_education`, `_parse_projects` را بر اساس فرمت رزومه خودتان سفارشی کنید

## مثال استفاده

```bash
# 1. ابتدا فقط محتوا را استخراج کنید
python manage.py update_from_cv --extract-only

# 2. فایل cv_content.txt را بررسی کنید

# 3. اگر محتوا درست است، به‌روزرسانی کنید
python manage.py update_from_cv

# 4. به Django Admin بروید و ترجمه‌های فارسی را اضافه کنید
```

## Troubleshooting

### خطا: PDF file not found
- مطمئن شوید فایل `my-cv-fa.pdf` در root پروژه است
- یا مسیر کامل را با `--pdf-path` مشخص کنید:
  ```bash
  python manage.py update_from_cv --pdf-path /path/to/your/cv.pdf
  ```

### خطا: pdfplumber not installed
```bash
pip install pdfplumber
```

### Parser داده‌ها را به درستی استخراج نمی‌کند
- فایل `cv_content.txt` را بررسی کنید
- اگر فرمت رزومه شما متفاوت است، parser را سفارشی کنید
- یا داده‌ها را به صورت دستی در Django Admin اضافه کنید

