from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from portfolio.models import Skill, Experience, Education, Project, Contact


class Command(BaseCommand):
    help = 'Creates sample data for portfolio app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
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
            {
                'title_en': 'Junior Developer',
                'title_fa': 'توسعه‌دهنده مبتدی',
                'company': 'Digital Agency',
                'start_date': date(2019, 3, 1),
                'end_date': date(2020, 5, 31),
                'description_en': 'Started career as a junior developer. Learned web development fundamentals and worked on client projects.',
                'description_fa': 'شروع کار به عنوان توسعه‌دهنده مبتدی. یادگیری اصول توسعه وب و کار روی پروژه‌های مشتری.',
                'current': False,
                'order': 3
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
            {
                'degree_en': 'High School Diploma',
                'degree_fa': 'دیپلم دبیرستان',
                'university': 'High School',
                'start_date': date(2011, 9, 1),
                'end_date': date(2015, 6, 30),
                'description_en': 'Mathematics and Physics focus.',
                'description_fa': 'تمرکز بر ریاضیات و فیزیک.',
                'order': 2
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
            {
                'title_en': 'Weather Dashboard',
                'title_fa': 'داشبورد آب و هوا',
                'description_en': 'A weather dashboard that displays current weather and forecasts using weather API.',
                'description_fa': 'داشبورد آب و هوا که وضعیت فعلی و پیش‌بینی را با استفاده از API آب و هوا نمایش می‌دهد.',
                'technologies': 'React, Weather API, Chart.js',
                'github_link': 'https://github.com/example/weather',
                'demo_link': 'https://weather-demo.example.com',
                'featured': False,
                'order': 4
            },
            {
                'title_en': 'Portfolio Website',
                'title_fa': 'وب‌سایت پورتفولیو',
                'description_en': 'A responsive portfolio website built with Django and Bootstrap, featuring bilingual support.',
                'description_fa': 'وب‌سایت پورتفولیو ریسپانسیو ساخته شده با Django و Bootstrap با پشتیبانی دو زبانه.',
                'technologies': 'Django, Bootstrap 5, i18n',
                'github_link': 'https://github.com/example/portfolio',
                'demo_link': 'https://portfolio.example.com',
                'featured': False,
                'order': 5
            },
        ]
        
        for proj_data in projects_data:
            Project.objects.get_or_create(
                title_en=proj_data['title_en'],
                defaults=proj_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects_data)} projects'))
        
        # Create Contact messages (optional sample data)
        contact_data = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'subject': 'Project Inquiry',
                'message': 'Hello, I am interested in working with you on a project.',
                'read': False
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'subject': 'Collaboration Opportunity',
                'message': 'Would you like to collaborate on an open-source project?',
                'read': True
            },
        ]
        
        for contact_msg in contact_data:
            Contact.objects.get_or_create(
                email=contact_msg['email'],
                subject=contact_msg['subject'],
                defaults=contact_msg
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(contact_data)} contact messages'))
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

