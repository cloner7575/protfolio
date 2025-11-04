from django.db import models


# Models will be implemented in a later task

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name_en = models.CharField(max_length=100, verbose_name=_('Name (English)'))
    name_fa = models.CharField(max_length=100, blank=True, verbose_name=_('Name (Persian)'))
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name=_('Slug'))
    description_en = models.TextField(blank=True, verbose_name=_('Description (English)'))
    description_fa = models.TextField(blank=True, verbose_name=_('Description (Persian)'))
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name_en']
    
    def __str__(self):
        return self.name_en
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})
    
    def get_name(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.name_fa if language == 'fa' and self.name_fa else self.name_en
    
    def get_description(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.description_fa if language == 'fa' and self.description_fa else self.description_en


class BlogPost(models.Model):
    title_en = models.CharField(max_length=200, verbose_name=_('Title (English)'))
    title_fa = models.CharField(max_length=200, blank=True, verbose_name=_('Title (Persian)'))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_('Slug'))
    content_en = models.TextField(verbose_name=_('Content (English)'))
    content_fa = models.TextField(blank=True, verbose_name=_('Content (Persian)'))
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name=_('Featured Image'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    published = models.BooleanField(default=False, verbose_name=_('Published'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    
    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title_en
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def get_title(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.title_fa if language == 'fa' and self.title_fa else self.title_en
    
    def get_content(self, language=None):
        from django.utils.translation import get_language
        if language is None:
            language = get_language()
        return self.content_fa if language == 'fa' and self.content_fa else self.content_en
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
