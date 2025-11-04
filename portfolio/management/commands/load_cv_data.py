"""Management command برای بارگذاری داده‌های رزومه از JSON"""
import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from portfolio.models import Skill, Experience, Education, Project, Contact


class Command(BaseCommand):
    help = 'Load CV data from JSON file and replace existing data'

    def add_arguments(self, parser):
        parser.add_argument('--json-file', type=str, default='cv_data.json',
                          help='Path to JSON file with CV data')
        parser.add_argument('--json-data', type=str, default=None,
                          help='JSON data as string (alternative to file)')
        parser.add_argument('--keep-existing', action='store_true',
                          help='Keep existing data instead of clearing')

    def handle(self, *args, **options):
        json_file = options['json_file']
        json_data_str = options['json_data']
        keep_existing = options['keep_existing']
        
        # Load JSON data
        if json_data_str:
            try:
                data = json.loads(json_data_str)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'Invalid JSON data: {e}'))
                return
        else:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f'JSON file not found: {json_file}'))
                self.stdout.write(self.style.WARNING('You can also pass JSON data directly with --json-data'))
                return
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'Invalid JSON file: {e}'))
                return
        
        # Clear existing data if not keeping
        if not keep_existing:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Skill.objects.all().delete()
            Experience.objects.all().delete()
            Education.objects.all().delete()
            Project.objects.all().delete()
            Contact.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))
        
        # Load Skills
        if 'skills' in data:
            self.stdout.write(self.style.SUCCESS('\n=== Loading Skills ==='))
            skills_created = 0
            skills_updated = 0
            
            for skill_data in data['skills']:
                skill, created = Skill.objects.get_or_create(
                    name=skill_data['name'],
                    defaults={
                        'category': skill_data.get('category', 'other'),
                        'level': skill_data.get('level', 50),
                        'icon': skill_data.get('icon', 'bi-code-slash'),
                        'order': skill_data.get('order', 0),
                    }
                )
                
                if not created:
                    # Update existing skill
                    skill.category = skill_data.get('category', skill.category)
                    skill.level = skill_data.get('level', skill.level)
                    skill.icon = skill_data.get('icon', skill.icon)
                    skill.order = skill_data.get('order', skill.order)
                    skill.save()
                    skills_updated += 1
                    self.stdout.write(f'  ✓ Updated: {skill.name}')
                else:
                    skills_created += 1
                    self.stdout.write(f'  ✓ Created: {skill.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Skills: {skills_created} created, {skills_updated} updated'))
        
        # Load Experiences
        if 'experiences' in data:
            self.stdout.write(self.style.SUCCESS('\n=== Loading Experiences ==='))
            exp_created = 0
            exp_updated = 0
            
            for exp_data in data['experiences']:
                # Parse dates
                start_date = parse_date(exp_data['start_date']) if exp_data.get('start_date') else None
                end_date = parse_date(exp_data['end_date']) if exp_data.get('end_date') else None
                
                exp, created = Experience.objects.get_or_create(
                    title_en=exp_data['title_en'],
                    company=exp_data['company'],
                    defaults={
                        'title_fa': exp_data.get('title_fa', ''),
                        'start_date': start_date,
                        'end_date': end_date,
                        'description_en': exp_data.get('description_en', ''),
                        'description_fa': exp_data.get('description_fa', ''),
                        'current': exp_data.get('current', False),
                        'order': exp_data.get('order', 0),
                    }
                )
                
                if not created:
                    exp.title_fa = exp_data.get('title_fa', exp.title_fa)
                    exp.start_date = start_date
                    exp.end_date = end_date
                    exp.description_en = exp_data.get('description_en', exp.description_en)
                    exp.description_fa = exp_data.get('description_fa', exp.description_fa)
                    exp.current = exp_data.get('current', exp.current)
                    exp.order = exp_data.get('order', exp.order)
                    exp.save()
                    exp_updated += 1
                    self.stdout.write(f'  ✓ Updated: {exp.title_en} at {exp.company}')
                else:
                    exp_created += 1
                    self.stdout.write(f'  ✓ Created: {exp.title_en} at {exp.company}')
            
            self.stdout.write(self.style.SUCCESS(f'Experiences: {exp_created} created, {exp_updated} updated'))
        
        # Load Education
        if 'educations' in data:
            self.stdout.write(self.style.SUCCESS('\n=== Loading Education ==='))
            edu_created = 0
            edu_updated = 0
            
            for edu_data in data['educations']:
                # Parse dates
                start_date = parse_date(edu_data['start_date']) if edu_data.get('start_date') else None
                end_date = parse_date(edu_data['end_date']) if edu_data.get('end_date') else None
                
                edu, created = Education.objects.get_or_create(
                    degree_en=edu_data['degree_en'],
                    university=edu_data['university'],
                    defaults={
                        'degree_fa': edu_data.get('degree_fa', ''),
                        'start_date': start_date,
                        'end_date': end_date,
                        'description_en': edu_data.get('description_en', ''),
                        'description_fa': edu_data.get('description_fa', ''),
                        'order': edu_data.get('order', 0),
                    }
                )
                
                if not created:
                    edu.degree_fa = edu_data.get('degree_fa', edu.degree_fa)
                    edu.start_date = start_date
                    edu.end_date = end_date
                    edu.description_en = edu_data.get('description_en', edu.description_en)
                    edu.description_fa = edu_data.get('description_fa', edu.description_fa)
                    edu.order = edu_data.get('order', edu.order)
                    edu.save()
                    edu_updated += 1
                    self.stdout.write(f'  ✓ Updated: {edu.degree_en} - {edu.university}')
                else:
                    edu_created += 1
                    self.stdout.write(f'  ✓ Created: {edu.degree_en} - {edu.university}')
            
            self.stdout.write(self.style.SUCCESS(f'Education: {edu_created} created, {edu_updated} updated'))
        
        # Load Projects
        if 'projects' in data:
            self.stdout.write(self.style.SUCCESS('\n=== Loading Projects ==='))
            proj_created = 0
            proj_updated = 0
            
            for proj_data in data['projects']:
                proj, created = Project.objects.get_or_create(
                    title_en=proj_data['title_en'],
                    defaults={
                        'title_fa': proj_data.get('title_fa', ''),
                        'description_en': proj_data.get('description_en', ''),
                        'description_fa': proj_data.get('description_fa', ''),
                        'github_link': proj_data.get('github_link', ''),
                        'demo_link': proj_data.get('demo_link', ''),
                        'technologies': proj_data.get('technologies', ''),
                        'featured': proj_data.get('featured', False),
                        'order': proj_data.get('order', 0),
                    }
                )
                
                if not created:
                    proj.title_fa = proj_data.get('title_fa', proj.title_fa)
                    proj.description_en = proj_data.get('description_en', proj.description_en)
                    proj.description_fa = proj_data.get('description_fa', proj.description_fa)
                    proj.github_link = proj_data.get('github_link', proj.github_link)
                    proj.demo_link = proj_data.get('demo_link', proj.demo_link)
                    proj.technologies = proj_data.get('technologies', proj.technologies)
                    proj.featured = proj_data.get('featured', proj.featured)
                    proj.order = proj_data.get('order', proj.order)
                    proj.save()
                    proj_updated += 1
                    self.stdout.write(f'  ✓ Updated: {proj.title_en}')
                else:
                    proj_created += 1
                    self.stdout.write(f'  ✓ Created: {proj.title_en}')
            
            self.stdout.write(self.style.SUCCESS(f'Projects: {proj_created} created, {proj_updated} updated'))
        
        # Load Contact (optional - usually just one example)
        if 'contact' in data:
            self.stdout.write(self.style.SUCCESS('\n=== Loading Contact Info ==='))
            contact_data = data['contact']
            # Note: Contact is usually for messages, but we can add a sample
            contact, created = Contact.objects.get_or_create(
                email=contact_data.get('email', ''),
                subject=contact_data.get('subject', ''),
                defaults={
                    'name': contact_data.get('name', ''),
                    'message': contact_data.get('message', ''),
                    'read': contact_data.get('read', False),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created contact: {contact.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Contact already exists: {contact.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All CV data loaded successfully!'))

