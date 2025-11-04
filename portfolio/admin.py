from django.contrib import admin
from .models import Skill, Experience, Education, Project, Contact


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'order']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'company', 'start_date', 'end_date', 'current', 'order']
    list_filter = ['current', 'start_date']
    search_fields = ['title_en', 'title_fa', 'company']
    ordering = ['-start_date', '-order']
    date_hierarchy = 'start_date'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree_en', 'university', 'start_date', 'end_date', 'order']
    list_filter = ['start_date']
    search_fields = ['degree_en', 'degree_fa', 'university']
    ordering = ['-start_date', '-order']
    date_hierarchy = 'start_date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'featured', 'created_at', 'order']
    list_filter = ['featured', 'created_at']
    search_fields = ['title_en', 'title_fa', 'description_en', 'technologies']
    ordering = ['-featured', '-created_at', 'order']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'created_at'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'read', 'created_at']
    list_filter = ['read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
