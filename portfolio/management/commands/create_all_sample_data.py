from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from portfolio.models import Skill, Experience, Education, Project, Contact
from blog.models import Category, BlogPost


class Command(BaseCommand):
    help = 'Creates sample data for both portfolio and blog apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data for portfolio and blog...'))
        
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
            self.stdout.write(self.style.SUCCESS('Created admin user (password: admin)'))
        
        # ========== PORTFOLIO DATA ==========
        self.stdout.write(self.style.WARNING('\n=== Creating Portfolio Data ==='))
        
        # Create Skills
        skills_data = [
            {'name': 'HTML/CSS', 'category': 'frontend', 'level': 90, 'icon': 'bi-code-slash', 'order': 1},
            {'name': 'JavaScript', 'category': 'frontend', 'level': 85, 'icon': 'bi-filetype-js', 'order': 2},
            {'name': 'React', 'category': 'frontend', 'level': 80, 'icon': 'bi-react', 'order': 3},
            {'name': 'Vue.js', 'category': 'frontend', 'level': 75, 'icon': 'bi-vuejs', 'order': 4},
            {'name': 'Python', 'category': 'backend', 'level': 90, 'icon': 'bi-filetype-py', 'order': 5},
            {'name': 'Django', 'category': 'backend', 'level': 88, 'icon': 'bi-gear', 'order': 6},
            {'name': 'FastAPI', 'category': 'backend', 'level': 75, 'icon': 'bi-lightning', 'order': 7},
            {'name': 'PostgreSQL', 'category': 'database', 'level': 80, 'icon': 'bi-database', 'order': 8},
            {'name': 'MySQL', 'category': 'database', 'level': 75, 'icon': 'bi-database', 'order': 9},
            {'name': 'MongoDB', 'category': 'database', 'level': 70, 'icon': 'bi-database', 'order': 10},
            {'name': 'Git', 'category': 'tools', 'level': 85, 'icon': 'bi-git', 'order': 11},
            {'name': 'Docker', 'category': 'tools', 'level': 75, 'icon': 'bi-box', 'order': 12},
        ]
        
        for skill_data in skills_data:
            Skill.objects.get_or_create(name=skill_data['name'], defaults=skill_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} skills'))
        
        # Create Experiences
        experiences_data = [
            {
                'title_en': 'Senior Full-Stack Developer',
                'title_fa': 'توسعه‌دهنده فول‌استک ارشد',
                'company': 'Tech Company Inc.',
                'start_date': date(2022, 1, 1),
                'end_date': None,
                'description_en': 'Lead development of web applications using Django and React. Manage team of 5 developers.',
                'description_fa': 'رهبری توسعه اپلیکیشن‌های وب با Django و React. مدیریت تیم 5 نفره توسعه‌دهندگان.',
                'current': True,
                'order': 1
            },
            {
                'title_en': 'Full-Stack Developer',
                'title_fa': 'توسعه‌دهنده فول‌استک',
                'company': 'Startup XYZ',
                'start_date': date(2020, 6, 1),
                'end_date': date(2021, 12, 31),
                'description_en': 'Developed and maintained multiple web applications. Worked with Python, JavaScript, and various frameworks.',
                'description_fa': 'توسعه و نگهداری چندین اپلیکیشن وب. کار با Python، JavaScript و فریمورک‌های مختلف.',
                'current': False,
                'order': 2
            },
        ]
        
        for exp_data in experiences_data:
            Experience.objects.get_or_create(
                title_en=exp_data['title_en'],
                company=exp_data['company'],
                defaults=exp_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(experiences_data)} experiences'))
        
        # Create Education
        education_data = [
            {
                'degree_en': 'Bachelor of Computer Science',
                'degree_fa': 'کارشناسی علوم کامپیوتر',
                'university': 'University of Technology',
                'start_date': date(2015, 9, 1),
                'end_date': date(2019, 6, 30),
                'description_en': 'Focused on software engineering, algorithms, and web development.',
                'description_fa': 'تمرکز بر مهندسی نرم‌افزار، الگوریتم‌ها و توسعه وب.',
                'order': 1
            },
        ]
        
        for edu_data in education_data:
            Education.objects.get_or_create(
                degree_en=edu_data['degree_en'],
                university=edu_data['university'],
                defaults=edu_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(education_data)} education records'))
        
        # Create Projects
        projects_data = [
            {
                'title_en': 'E-Commerce Platform',
                'title_fa': 'پلتفرم تجارت الکترونیک',
                'description_en': 'A full-featured e-commerce platform with user authentication, shopping cart, payment integration, and admin panel.',
                'description_fa': 'پلتفرم تجارت الکترونیک کامل با احراز هویت کاربر، سبد خرید، یکپارچه‌سازی پرداخت و پنل ادمین.',
                'technologies': 'Django, React, PostgreSQL, Stripe API',
                'github_link': 'https://github.com/example/ecommerce',
                'demo_link': 'https://ecommerce-demo.example.com',
                'featured': True,
                'order': 1
            },
            {
                'title_en': 'Task Management App',
                'title_fa': 'اپلیکیشن مدیریت کارها',
                'description_en': 'A collaborative task management application with real-time updates, team workspaces, and notification system.',
                'description_fa': 'اپلیکیشن مدیریت کار تیمی با به‌روزرسانی لحظه‌ای، فضای کاری تیمی و سیستم اطلاع‌رسانی.',
                'technologies': 'Django REST Framework, Vue.js, WebSocket, Redis',
                'github_link': 'https://github.com/example/taskmanager',
                'demo_link': 'https://tasks-demo.example.com',
                'featured': True,
                'order': 2
            },
            {
                'title_en': 'Blog Platform',
                'title_fa': 'پلتفرم بلاگ',
                'description_en': 'A modern blogging platform with markdown support, categories, tags, and comment system.',
                'description_fa': 'پلتفرم بلاگ مدرن با پشتیبانی markdown، دسته‌بندی، تگ و سیستم کامنت.',
                'technologies': 'Django, Bootstrap, JavaScript',
                'github_link': 'https://github.com/example/blog',
                'demo_link': 'https://blog-demo.example.com',
                'featured': False,
                'order': 3
            },
        ]
        
        for proj_data in projects_data:
            Project.objects.get_or_create(
                title_en=proj_data['title_en'],
                defaults=proj_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects_data)} projects'))
        
        # ========== BLOG DATA ==========
        self.stdout.write(self.style.WARNING('\n=== Creating Blog Data ==='))
        
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
                'content_en': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.',
                'content_fa': 'Django یک فریمورک وب سطح بالا برای Python است که توسعه سریع و طراحی تمیز و کاربردی را تشویق می‌کند.',
                'category': categories[2],  # Django
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=5),
                'views': 150
            },
            {
                'title_en': 'Building REST APIs with Django REST Framework',
                'title_fa': 'ساخت REST API با Django REST Framework',
                'content_en': 'Django REST Framework (DRF) makes it easy to build Web APIs for your Django-based applications.',
                'content_fa': 'Django REST Framework (DRF) ساخت Web API برای اپلیکیشن‌های مبتنی بر Django را آسان می‌کند.',
                'category': categories[1],  # Python
                'author': user,
                'published': True,
                'created_at': now - timedelta(days=10),
                'views': 320
            },
        ]
        
        for post_data in blog_posts_data:
            BlogPost.objects.get_or_create(
                title_en=post_data['title_en'],
                defaults=post_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(blog_posts_data)} blog posts'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All sample data created successfully!'))

