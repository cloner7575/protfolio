from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from .models import Skill, Experience, Education, Project, Contact, Profile
from .forms import ContactForm
from blog.models import BlogPost


def home(request):
    """Home page with hero section, latest projects and blog posts"""
    language = get_language()
    featured_projects = Project.objects.filter(featured=True)[:3]
    latest_projects = Project.objects.all()[:6]
    latest_posts = BlogPost.objects.filter(published=True)[:3]
    profile = Profile.get_profile()
    
    context = {
        'featured_projects': featured_projects,
        'latest_projects': latest_projects,
        'latest_posts': latest_posts,
        'language': language,
        'profile': profile,
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    """About page with personal information and skills"""
    language = get_language()
    skills = Skill.objects.all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    profile = Profile.get_profile()
    
    context = {
        'skills_by_category': skills_by_category,
        'language': language,
        'profile': profile,
    }
    return render(request, 'portfolio/about.html', context)


def skills(request):
    """Skills page"""
    language = get_language()
    skills = Skill.objects.all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category,
        'language': language,
    }
    return render(request, 'portfolio/skills.html', context)


def experience(request):
    """Experience page with timeline"""
    language = get_language()
    experiences = Experience.objects.all()
    
    context = {
        'experiences': experiences,
        'language': language,
    }
    return render(request, 'portfolio/experience.html', context)


def education(request):
    """Education page with timeline"""
    language = get_language()
    educations = Education.objects.all()
    
    context = {
        'educations': educations,
        'language': language,
    }
    return render(request, 'portfolio/education.html', context)


def projects(request):
    """Projects list page with filtering"""
    language = get_language()
    projects_list = Project.objects.all()
    
    # Filter by technology if provided
    technology = request.GET.get('technology', None)
    if technology:
        projects_list = projects_list.filter(technologies__icontains=technology)
    
    # Get all unique technologies for filter
    all_projects = Project.objects.all()
    all_technologies = set()
    for project in all_projects:
        tech_list = project.get_technologies_list()
        all_technologies.update(tech_list)
    all_technologies = sorted(list(all_technologies))
    
    context = {
        'projects': projects_list,
        'all_technologies': all_technologies,
        'selected_technology': technology,
        'language': language,
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail(request, slug):
    """Project detail page"""
    language = get_language()
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'language': language,
    }
    return render(request, 'portfolio/project_detail.html', context)


def contact(request):
    """Contact page with form"""
    language = get_language()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email
            try:
                send_mail(
                    subject=f"Portfolio Contact: {contact_message.subject}",
                    message=f"Name: {contact_message.name}\nEmail: {contact_message.email}\n\nMessage:\n{contact_message.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, _('Your message has been sent successfully!'))
            except Exception as e:
                messages.error(request, _('There was an error sending your message. Please try again later.'))
            
            form = ContactForm()  # Reset form
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'language': language,
    }
    return render(request, 'portfolio/contact.html', context)
