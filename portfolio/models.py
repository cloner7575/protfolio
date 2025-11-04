from django.db import models


# Models will be implemented in a later task

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('frontend', _('Frontend')),
        ('backend', _('Backend')),
        ('database', _('Database')),
        ('tools', _('Tools')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, verbose_name=_('Category'))
    level = models.IntegerField(default=0, help_text=_('Percentage (0-100)'), verbose_name=_('Level'))
    icon = models.CharField(max_length=100, blank=True, help_text=_('Icon class name (e.g., fa fa-html5)'), verbose_name=_('Icon'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Experience(models.Model):
    title_en = models.CharField(max_length=200, verbose_name=_('Title (English)'))
    title_fa = models.CharField(max_length=200, blank=True, verbose_name=_('Title (Persian)'))
    company = models.CharField(max_length=200, verbose_name=_('Company'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    description_en = models.TextField(verbose_name=_('Description (English)'))
    description_fa = models.TextField(blank=True, verbose_name=_('Description (Persian)'))
    current = models.BooleanField(default=False, verbose_name=_('Current Position'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    
    class Meta:
        verbose_name = _('Experience')
        verbose_name_plural = _('Experiences')
        ordering = ['-start_date', '-order']
    
    def __str__(self):
        return f"{self.title_en} at {self.company}"
    
    def get_title(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.title_fa if language == 'fa' and self.title_fa else self.title_en
    
    def get_description(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.description_fa if language == 'fa' and self.description_fa else self.description_en


class Education(models.Model):
    degree_en = models.CharField(max_length=200, verbose_name=_('Degree (English)'))
    degree_fa = models.CharField(max_length=200, blank=True, verbose_name=_('Degree (Persian)'))
    university = models.CharField(max_length=200, verbose_name=_('University'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    description_en = models.TextField(blank=True, verbose_name=_('Description (English)'))
    description_fa = models.TextField(blank=True, verbose_name=_('Description (Persian)'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    
    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')
        ordering = ['-start_date', '-order']
    
    def __str__(self):
        return f"{self.degree_en} - {self.university}"
    
    def get_degree(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.degree_fa if language == 'fa' and self.degree_fa else self.degree_en
    
    def get_description(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.description_fa if language == 'fa' and self.description_fa else self.description_en


class Project(models.Model):
    title_en = models.CharField(max_length=200, verbose_name=_('Title (English)'))
    title_fa = models.CharField(max_length=200, blank=True, verbose_name=_('Title (Persian)'))
    description_en = models.TextField(verbose_name=_('Description (English)'))
    description_fa = models.TextField(blank=True, verbose_name=_('Description (Persian)'))
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name=_('Image'))
    github_link = models.URLField(blank=True, verbose_name=_('GitHub Link'))
    demo_link = models.URLField(blank=True, verbose_name=_('Demo Link'))
    technologies = models.CharField(max_length=500, help_text=_('Comma-separated list'), verbose_name=_('Technologies'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_('Slug'))
    
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-featured', '-created_at', 'order']
    
    def __str__(self):
        return self.title_en
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def get_title(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.title_fa if language == 'fa' and self.title_fa else self.title_en
    
    def get_description(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.description_fa if language == 'fa' and self.description_fa else self.description_en
    
    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    message = models.TextField(verbose_name=_('Message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    read = models.BooleanField(default=False, verbose_name=_('Read'))
    
    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
