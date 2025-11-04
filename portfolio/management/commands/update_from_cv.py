"""Management command برای به‌روزرسانی محتوای سایت بر اساس رزومه - دو زبانه"""
from django.core.management.base import BaseCommand
import os
import sys
import re
from datetime import date, datetime

# Try to import pdfplumber
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

from portfolio.models import Skill, Experience, Education, Project


class Command(BaseCommand):
    help = 'Read CV PDF and update portfolio content (Skills, Experience, Education, Projects) - Bilingual'

    def add_arguments(self, parser):
        parser.add_argument('--pdf-path', type=str, default='my-cv-fa.pdf',
                          help='Path to CV PDF file')
        parser.add_argument('--clear-existing', action='store_true',
                          help='Clear existing data before updating')
        parser.add_argument('--extract-only', action='store_true',
                          help='Only extract text from PDF without updating database')

    def handle(self, *args, **options):
        pdf_path = options['pdf_path']
        clear_existing = options['clear_existing']
        extract_only = options['extract_only']
        
        # Check if pdfplumber is available, install if needed
        if not PDFPLUMBER_AVAILABLE:
            self.stdout.write(self.style.WARNING('pdfplumber is not installed. Installing...'))
            os.system(f"{sys.executable} -m pip install pdfplumber -q")
            try:
                import pdfplumber
            except ImportError:
                self.stdout.write(self.style.ERROR('Failed to install pdfplumber. Please install manually: pip install pdfplumber'))
                return
        else:
            # Import if it was available at module level
            import pdfplumber
        
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'PDF file not found: {pdf_path}'))
            self.stdout.write(self.style.WARNING('Please make sure the PDF file exists in the project root.'))
            return
        
        # Extract text from PDF
        self.stdout.write(self.style.SUCCESS(f'Reading CV from: {pdf_path}'))
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ''
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
            
            # Save extracted text
            with open('cv_content.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            
            self.stdout.write(self.style.SUCCESS('✓ CV content extracted successfully!'))
            self.stdout.write(self.style.SUCCESS('✓ Content saved to cv_content.txt'))
            
            if extract_only:
                self.stdout.write('\n' + '='*60)
                self.stdout.write('EXTRACTED CONTENT:')
                self.stdout.write('='*60)
                self.stdout.write(text[:1000] + '...' if len(text) > 1000 else text)
                self.stdout.write('='*60)
                return
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading PDF: {e}'))
            import traceback
            traceback.print_exc()
            return
        
        # Parse and update content
        self.stdout.write(self.style.WARNING('\n=== Parsing CV Content ==='))
        
        # Clear existing data if requested
        if clear_existing:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Skill.objects.all().delete()
            Experience.objects.all().delete()
            Education.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))
        
        # Parse content from text
        skills = self._parse_skills(text)
        experiences = self._parse_experiences(text)
        education = self._parse_education(text)
        projects = self._parse_projects(text)
        
        # Update database
        self._update_skills(skills)
        self._update_experiences(experiences)
        self._update_education(education)
        self._update_projects(projects)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Portfolio updated from CV!'))
        self.stdout.write(self.style.WARNING('\n📝 Please review the data in Django admin and make adjustments if needed.'))

    def _parse_skills(self, text):
        """Parse skills from CV text - returns list of dicts with bilingual info"""
        skills = []
        text_lower = text.lower()
        
        # Define skill mappings with bilingual info
        skill_mappings = {
            # Programming Languages
            'python': {'name': 'Python', 'category': 'backend', 'level': 90, 'icon': 'bi-filetype-py'},
            'javascript': {'name': 'JavaScript', 'category': 'frontend', 'level': 85, 'icon': 'bi-filetype-js'},
            'typescript': {'name': 'TypeScript', 'category': 'frontend', 'level': 80, 'icon': 'bi-filetype-js'},
            'java': {'name': 'Java', 'category': 'backend', 'level': 75, 'icon': 'bi-filetype-java'},
            'php': {'name': 'PHP', 'category': 'backend', 'level': 70, 'icon': 'bi-filetype-php'},
            'c++': {'name': 'C++', 'category': 'backend', 'level': 70, 'icon': 'bi-code-slash'},
            'c#': {'name': 'C#', 'category': 'backend', 'level': 70, 'icon': 'bi-code-slash'},
            
            # Web Frameworks
            'django': {'name': 'Django', 'category': 'backend', 'level': 90, 'icon': 'bi-gear'},
            'flask': {'name': 'Flask', 'category': 'backend', 'level': 85, 'icon': 'bi-lightning'},
            'fastapi': {'name': 'FastAPI', 'category': 'backend', 'level': 80, 'icon': 'bi-lightning'},
            'react': {'name': 'React', 'category': 'frontend', 'level': 85, 'icon': 'bi-react'},
            'vue': {'name': 'Vue.js', 'category': 'frontend', 'level': 80, 'icon': 'bi-vuejs'},
            'angular': {'name': 'Angular', 'category': 'frontend', 'level': 75, 'icon': 'bi-angular'},
            'node.js': {'name': 'Node.js', 'category': 'backend', 'level': 80, 'icon': 'bi-nodejs'},
            
            # Frontend
            'html': {'name': 'HTML/CSS', 'category': 'frontend', 'level': 95, 'icon': 'bi-code-slash'},
            'css': {'name': 'HTML/CSS', 'category': 'frontend', 'level': 95, 'icon': 'bi-brush'},
            'bootstrap': {'name': 'Bootstrap', 'category': 'frontend', 'level': 90, 'icon': 'bi-bootstrap'},
            'tailwind': {'name': 'Tailwind CSS', 'category': 'frontend', 'level': 85, 'icon': 'bi-brush'},
            'sass': {'name': 'SASS/SCSS', 'category': 'frontend', 'level': 80, 'icon': 'bi-brush'},
            
            # Databases
            'postgresql': {'name': 'PostgreSQL', 'category': 'database', 'level': 85, 'icon': 'bi-database'},
            'mysql': {'name': 'MySQL', 'category': 'database', 'level': 80, 'icon': 'bi-database'},
            'mongodb': {'name': 'MongoDB', 'category': 'database', 'level': 75, 'icon': 'bi-database'},
            'sqlite': {'name': 'SQLite', 'category': 'database', 'level': 85, 'icon': 'bi-database'},
            'redis': {'name': 'Redis', 'category': 'database', 'level': 75, 'icon': 'bi-database'},
            
            # Tools & DevOps
            'git': {'name': 'Git', 'category': 'tools', 'level': 90, 'icon': 'bi-git'},
            'docker': {'name': 'Docker', 'category': 'tools', 'level': 80, 'icon': 'bi-box'},
            'kubernetes': {'name': 'Kubernetes', 'category': 'tools', 'level': 70, 'icon': 'bi-box'},
            'linux': {'name': 'Linux', 'category': 'tools', 'level': 85, 'icon': 'bi-terminal'},
            'nginx': {'name': 'Nginx', 'category': 'tools', 'level': 75, 'icon': 'bi-server'},
            'aws': {'name': 'AWS', 'category': 'tools', 'level': 75, 'icon': 'bi-cloud'},
            'azure': {'name': 'Azure', 'category': 'tools', 'level': 70, 'icon': 'bi-cloud'},
        }
        
        # Check for skills in text
        found_skills = {}
        for skill_key, skill_info in skill_mappings.items():
            if skill_key in text_lower:
                skill_name = skill_info['name']
                if skill_name not in found_skills:
                    found_skills[skill_name] = skill_info.copy()
        
        # Convert to list
        for i, (skill_name, skill_info) in enumerate(found_skills.items(), 1):
            skills.append({
                'name': skill_name,
                'category': skill_info['category'],
                'level': skill_info['level'],
                'icon': skill_info['icon'],
                'order': i
            })
        
        return skills

    def _parse_experiences(self, text):
        """Parse work experience from CV text - returns list of dicts with bilingual info"""
        experiences = []
        
        # Common patterns for experience section
        exp_patterns = [
            r'(?i)(?:work\s+experience|تجربه\s+کاری|سابقه\s+کار|experience)[\s:]*\n(.*?)(?=\n(?:education|تحصیلات|skills|مهارت|projects|پروژه)|$)',
            r'(?i)(?:position|موقعیت|شغل)[\s:]*([^\n]+)',
        ]
        
        # Try to extract experiences
        # This is a simplified parser - you may need to customize based on your CV format
        # Look for date patterns
        date_pattern = r'(\d{4})[-\s]*(?:to|تا|present|اکنون|current|فعلی)?\s*(\d{4})?'
        
        # Look for company names (capitalized words)
        company_pattern = r'([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Ltd|Company|Corp)?)'
        
        # Extract potential experiences
        lines = text.split('\n')
        current_exp = None
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check if line contains a date (likely start of experience)
            date_match = re.search(date_pattern, line)
            if date_match:
                if current_exp:
                    experiences.append(current_exp)
                
                start_year = int(date_match.group(1))
                end_year = int(date_match.group(2)) if date_match.group(2) else None
                
                current_exp = {
                    'title_en': '',
                    'title_fa': '',
                    'company': '',
                    'start_date': date(start_year, 1, 1),
                    'end_date': date(end_year, 12, 31) if end_year else None,
                    'description_en': '',
                    'description_fa': '',
                    'current': end_year is None,
                    'order': len(experiences) + 1
                }
            
            # Check for company name
            if current_exp and not current_exp['company']:
                company_match = re.search(company_pattern, line)
                if company_match:
                    current_exp['company'] = company_match.group(1).strip()
            
            # Check for job title (usually before company or date)
            if current_exp and not current_exp['title_en']:
                # Look for common job title patterns
                line_lower = line.lower()
                title_keywords = ['developer', 'engineer', 'programmer', 'توسعه', 'مهندس', 'برنامه‌نویس']
                if any(keyword in line_lower for keyword in title_keywords):
                    current_exp['title_en'] = line_stripped
                    current_exp['title_fa'] = line_stripped  # You'll need to translate manually
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences

    def _parse_education(self, text):
        """Parse education from CV text - returns list of dicts with bilingual info"""
        education = []
        
        # Look for education section
        edu_pattern = r'(?i)(?:education|تحصیلات|degree|مدرک)[\s:]*\n(.*?)(?=\n(?:experience|تجربه|skills|مهارت|projects|پروژه)|$)'
        
        # Look for degree patterns
        degree_patterns = [
            r'(?i)(?:bachelor|کارشناسی|B\.?S\.?|B\.?A\.?|B\.?Sc\.?)',
            r'(?i)(?:master|کارشناسی\s+ارشد|M\.?S\.?|M\.?A\.?|M\.?Sc\.?)',
            r'(?i)(?:phd|دکتری|Ph\.?D\.?|Doctorate)',
        ]
        
        # Look for university names
        university_pattern = r'(?i)(?:university|دانشگاه|college|کالج)[\s:]+([A-Z][^\n]+)'
        
        lines = text.split('\n')
        current_edu = None
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check for degree
            for pattern in degree_patterns:
                if re.search(pattern, line):
                    if current_edu:
                        education.append(current_edu)
                    
                    current_edu = {
                        'degree_en': line_stripped,
                        'degree_fa': line_stripped,  # You'll need to translate manually
                        'university': '',
                        'start_date': date(2015, 9, 1),  # Default - adjust manually
                        'end_date': date(2019, 6, 30),  # Default - adjust manually
                        'description_en': '',
                        'description_fa': '',
                        'order': len(education) + 1
                    }
                    break
            
            # Check for university
            if current_edu and not current_edu['university']:
                uni_match = re.search(university_pattern, line)
                if uni_match:
                    current_edu['university'] = uni_match.group(1).strip()
        
        if current_edu:
            education.append(current_edu)
        
        return education

    def _parse_projects(self, text):
        """Parse projects from CV text - returns list of dicts with bilingual info"""
        projects = []
        
        # Look for projects section
        proj_pattern = r'(?i)(?:projects|پروژه|project)[\s:]*\n(.*?)(?=\n(?:experience|تجربه|education|تحصیلات|skills|مهارت)|$)'
        
        # Look for project indicators
        project_keywords = ['project', 'پروژه', 'app', 'application', 'اپلیکیشن', 'website', 'وب‌سایت', 'system', 'سیستم']
        
        lines = text.split('\n')
        current_proj = None
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                if current_proj:
                    projects.append(current_proj)
                    current_proj = None
                continue
            
            # Check if line mentions a project
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                if current_proj:
                    projects.append(current_proj)
                
                current_proj = {
                    'title_en': line_stripped,
                    'title_fa': line_stripped,  # You'll need to translate manually
                    'description_en': '',
                    'description_fa': '',
                    'technologies': '',
                    'github_link': '',
                    'demo_link': '',
                    'featured': False,
                    'order': len(projects) + 1
                }
            elif current_proj:
                # Add to description
                if not current_proj['description_en']:
                    current_proj['description_en'] = line_stripped
                    current_proj['description_fa'] = line_stripped
        
        if current_proj:
            projects.append(current_proj)
        
        return projects

    def _update_skills(self, skills):
        """Update skills in database"""
        if not skills:
            self.stdout.write(self.style.WARNING('⚠ No skills found in CV'))
            return
        
        updated = 0
        created = 0
        for skill_data in skills:
            skill, created_flag = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created skill: {skill.name} ({skill.category})'))
            else:
                # Update existing skill
                for key, value in skill_data.items():
                    setattr(skill, key, value)
                skill.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated skill: {skill.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Skills: {created} created, {updated} updated'))

    def _update_experiences(self, experiences):
        """Update experiences in database"""
        if not experiences:
            self.stdout.write(self.style.WARNING('⚠ No experiences found in CV'))
            self.stdout.write(self.style.WARNING('  You may need to add them manually in Django admin.'))
            return
        
        updated = 0
        created = 0
        for exp_data in experiences:
            # Skip if essential fields are missing
            if not exp_data.get('title_en') or not exp_data.get('company'):
                continue
            
            exp, created_flag = Experience.objects.get_or_create(
                title_en=exp_data['title_en'],
                company=exp_data['company'],
                defaults=exp_data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created experience: {exp.title_en} at {exp.company}'))
            else:
                for key, value in exp_data.items():
                    setattr(exp, key, value)
                exp.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated experience: {exp.title_en}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Experiences: {created} created, {updated} updated'))

    def _update_education(self, education):
        """Update education in database"""
        if not education:
            self.stdout.write(self.style.WARNING('⚠ No education found in CV'))
            self.stdout.write(self.style.WARNING('  You may need to add it manually in Django admin.'))
            return
        
        updated = 0
        created = 0
        for edu_data in education:
            # Skip if essential fields are missing
            if not edu_data.get('degree_en') or not edu_data.get('university'):
                continue
            
            edu, created_flag = Education.objects.get_or_create(
                degree_en=edu_data['degree_en'],
                university=edu_data['university'],
                defaults=edu_data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created education: {edu.degree_en} - {edu.university}'))
            else:
                for key, value in edu_data.items():
                    setattr(edu, key, value)
                edu.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated education: {edu.degree_en}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Education: {created} created, {updated} updated'))

    def _update_projects(self, projects):
        """Update projects in database"""
        if not projects:
            self.stdout.write(self.style.WARNING('⚠ No projects found in CV'))
            self.stdout.write(self.style.WARNING('  You may need to add them manually in Django admin.'))
            return
        
        updated = 0
        created = 0
        for proj_data in projects:
            # Skip if essential fields are missing
            if not proj_data.get('title_en'):
                continue
            
            proj, created_flag = Project.objects.get_or_create(
                title_en=proj_data['title_en'],
                defaults=proj_data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created project: {proj.title_en}'))
            else:
                for key, value in proj_data.items():
                    setattr(proj, key, value)
                proj.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated project: {proj.title_en}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Projects: {created} created, {updated} updated'))
