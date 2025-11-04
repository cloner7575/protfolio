from django.contrib import admin
from .models import Category, BlogPost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'slug']
    search_fields = ['name_en', 'name_fa']
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'author', 'category', 'published', 'views', 'created_at']
    list_filter = ['published', 'category', 'created_at', 'author']
    search_fields = ['title_en', 'title_fa', 'content_en', 'content_fa']
    prepopulated_fields = {'slug': ('title_en',)}
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title_en', 'title_fa', 'slug', 'content_en', 'content_fa', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'published')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
