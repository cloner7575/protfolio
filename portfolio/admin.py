from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Skill, Experience, Education, Project, Contact, Profile


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name_en', 'name_fa', 'profile_image', 'title_en', 'title_fa')
        }),
        (_('Biography'), {
            'fields': ('bio_short_en', 'bio_short_fa', 'bio_long_en', 'bio_long_fa')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'location')
        }),
        (_('Social Links'), {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'website_url')
        }),
        (_('Statistics'), {
            'fields': ('years_experience', 'projects_completed')
        }),
        (_('Metadata'), {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Only allow one profile instance
        return not Profile.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of profile
        return False
