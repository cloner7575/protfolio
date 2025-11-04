from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from blog.models import Category, BlogPost


class Command(BaseCommand):
    help = 'Creates sample data for blog app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample blog data...'))
        
        # Get or create a user for blog posts
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
            }
        )
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create Categories
        categories_data = [
            {
                'name_en': 'Web Development',
                'name_fa': 'توسعه وب',
                'description_en': 'Articles about web development, frameworks, and best practices.',
                'description_fa': 'مقالات درباره توسعه وب، فریمورک‌ها و بهترین روش‌ها.'
            },
            {
                'name_en': 'Python',
                'name_fa': 'پایتون',
                'description_en': 'Python programming tips, tutorials, and news.',
                'description_fa': 'نکات، آموزش‌ها و اخبار برنامه‌نویسی پایتون.'
            },
            {
                'name_en': 'Django',
                'name_fa': 'جنگو',
                'description_en': 'Django framework tutorials and guides.',
                'description_fa': 'آموزش‌ها و راهنماهای فریمورک Django.'
            },
            {
                'name_en': 'Frontend',
                'name_fa': 'فرانت‌اند',
                'description_en': 'Frontend development with React, Vue, and modern JavaScript.',
                'description_fa': 'توسعه فرانت‌اند با React، Vue و JavaScript مدرن.'
            },
            {
                'name_en': 'Tutorials',
                'name_fa': 'آموزش‌ها',
                'description_en': 'Step-by-step tutorials and guides.',
                'description_fa': 'آموزش‌ها و راهنماهای گام به گام.'
            },
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name_en=cat_data['name_en'],
                defaults=cat_data
            )
            categories.append(cat)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        
        # Create Blog Posts
        now = timezone.now()
        blog_posts_data = [
            {
                'title_en': 'Getting Started with Django',
                'title_fa': 'شروع کار با Django',
                'content_en': '''# Getting Started with Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this article, we'll cover the basics of setting up a Django project.

## Installation

First, install Django using pip:

\`\`\`bash
pip install django
\`\`\`

## Creating a Project

Create a new Django project:

\`\`\`bash
django-admin startproject myproject
\`\`\`

This will create a new directory with the basic Django project structure.

## Next Steps

- Create your first app
- Set up the database
- Create your first view

Stay tuned for more tutorials!''',
                'content_fa': '''# شروع کار با Django

Django یک فریمورک وب سطح بالا برای Python است که توسعه سریع و طراحی تمیز و کاربردی را تشویق می‌کند. در این مقاله، اصول راه‌اندازی یک پروژه Django را پوشش می‌دهیم.

## نصب

ابتدا Django را با pip نصب کنید:

\`\`\`bash
pip install django
\`\`\`

## ایجاد پروژه

یک پروژه Django جدید ایجاد کنید:

\`\`\`bash
django-admin startproject myproject
\`\`\`

این یک دایرکتوری جدید با ساختار پایه پروژه Django ایجاد می‌کند.

## مراحل بعدی

- ایجاد اولین اپ
- تنظیم دیتابیس
- ایجاد اولین view

برای آموزش‌های بیشتر با ما همراه باشید!''',
                'category': categories[2],  # Django
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=5),
                'views': 150
            },
            {
                'title_en': 'Building REST APIs with Django REST Framework',
                'title_fa': 'ساخت REST API با Django REST Framework',
                'content_en': '''# Building REST APIs with Django REST Framework

Django REST Framework (DRF) makes it easy to build Web APIs for your Django-based applications.

## Key Features

- Serializers for data validation
- ViewSets for CRUD operations
- Authentication and permissions
- Browsable API

## Getting Started

Install DRF:

\`\`\`bash
pip install djangorestframework
\`\`\`

Add it to your INSTALLED_APPS and start building your API!''',
                'content_fa': '''# ساخت REST API با Django REST Framework

Django REST Framework (DRF) ساخت Web API برای اپلیکیشن‌های مبتنی بر Django را آسان می‌کند.

## ویژگی‌های کلیدی

- Serializer برای اعتبارسنجی داده
- ViewSet برای عملیات CRUD
- احراز هویت و مجوزها
- API قابل مرور

## شروع کار

DRF را نصب کنید:

\`\`\`bash
pip install djangorestframework
\`\`\`

آن را به INSTALLED_APPS اضافه کنید و شروع به ساخت API خود کنید!''',
                'category': categories[1],  # Python
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=10),
                'views': 320
            },
            {
                'title_en': 'React Hooks: A Complete Guide',
                'title_fa': 'React Hooks: راهنمای کامل',
                'content_en': '''# React Hooks: A Complete Guide

React Hooks are functions that let you use state and other React features in functional components.

## Common Hooks

- **useState**: Manage component state
- **useEffect**: Handle side effects
- **useContext**: Access context values
- **useReducer**: Complex state management

## Example

\`\`\`javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
\`\`\`

Hooks make React code cleaner and more reusable!''',
                'content_fa': '''# React Hooks: راهنمای کامل

React Hooks توابعی هستند که به شما امکان استفاده از state و ویژگی‌های دیگر React را در کامپوننت‌های تابعی می‌دهند.

## Hooks رایج

- **useState**: مدیریت state کامپوننت
- **useEffect**: مدیریت side effects
- **useContext**: دسترسی به مقادیر context
- **useReducer**: مدیریت state پیچیده

## مثال

\`\`\`javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
\`\`\`

Hooks کد React را تمیزتر و قابل استفاده مجدد می‌کنند!''',
                'category': categories[3],  # Frontend
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=15),
                'views': 450
            },
            {
                'title_en': 'Database Optimization in Django',
                'title_fa': 'بهینه‌سازی دیتابیس در Django',
                'content_en': '''# Database Optimization in Django

Database performance is crucial for web applications. Here are some tips for optimizing your Django database queries.

## Use select_related and prefetch_related

\`\`\`python
# Bad
authors = Author.objects.all()
for author in authors:
    print(author.book.title)

# Good
authors = Author.objects.select_related('book').all()
for author in authors:
    print(author.book.title)
\`\`\`

## Add Database Indexes

Add indexes to frequently queried fields to speed up queries.

## Use QuerySet Methods Wisely

- `only()`: Load only needed fields
- `defer()`: Defer loading of certain fields
- `exists()`: Check existence without loading

Optimize your queries for better performance!''',
                'content_fa': '''# بهینه‌سازی دیتابیس در Django

عملکرد دیتابیس برای اپلیکیشن‌های وب بسیار مهم است. در اینجا نکاتی برای بهینه‌سازی کوئری‌های دیتابیس Django ارائه شده است.

## استفاده از select_related و prefetch_related

\`\`\`python
# بد
authors = Author.objects.all()
for author in authors:
    print(author.book.title)

# خوب
authors = Author.objects.select_related('book').all()
for author in authors:
    print(author.book.title)
\`\`\`

## افزودن ایندکس دیتابیس

ایندکس را به فیلدهایی که مکرراً کوئری می‌شوند اضافه کنید تا سرعت کوئری افزایش یابد.

## استفاده عاقلانه از متدهای QuerySet

- `only()`: بارگذاری فقط فیلدهای مورد نیاز
- `defer()`: به تأخیر انداختن بارگذاری فیلدهای خاص
- `exists()`: بررسی وجود بدون بارگذاری

کوئری‌های خود را برای عملکرد بهتر بهینه کنید!''',
                'category': categories[2],  # Django
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=20),
                'views': 280
            },
            {
                'title_en': 'Introduction to Python Decorators',
                'title_fa': 'معرفی Decoratorهای Python',
                'content_en': '''# Introduction to Python Decorators

Decorators are a powerful feature in Python that allow you to modify the behavior of functions.

## Basic Decorator

\`\`\`python
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
\`\`\`

## Use Cases

- Logging
- Timing functions
- Authentication
- Caching

Decorators make code more modular and reusable!''',
                'content_fa': '''# معرفی Decoratorهای Python

Decoratorها یک ویژگی قدرتمند در Python هستند که به شما امکان تغییر رفتار توابع را می‌دهند.

## Decorator پایه

\`\`\`python
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
\`\`\`

## موارد استفاده

- لاگینگ
- زمان‌سنجی توابع
- احراز هویت
- کش

Decoratorها کد را ماژولارتر و قابل استفاده مجدد می‌کنند!''',
                'category': categories[1],  # Python
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=25),
                'views': 520
            },
        ]
        
        for post_data in blog_posts_data:
            BlogPost.objects.get_or_create(
                title_en=post_data['title_en'],
                defaults=post_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(blog_posts_data)} blog posts'))
        
        self.stdout.write(self.style.SUCCESS('Sample blog data created successfully!'))

