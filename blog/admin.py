from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
import json
from .models import Category, BlogPost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fa', 'slug')
    search_fields = ('name_en', 'name_fa', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.import_json_view, name='category_import_json'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def import_json_view(self, request):
        if request.method == 'POST':
            json_file = request.FILES.get('json_file')

            if not json_file:
                messages.error(request, 'لطفا یک فایل انتخاب کنید')
                return redirect('..')

            try:
                data = json.load(json_file)

                # بررسی فرمت fixture یا ساختار قدیمی
                if isinstance(data, list):
                    # فرمت Django fixture
                    categories = [item for item in data if item.get('model') == 'blog.category']

                    imported_count = 0
                    for item in categories:
                        fields = item.get('fields', {})
                        Category.objects.update_or_create(
                            pk=item.get('pk'),
                            defaults={
                                'name_en': fields.get('name_en', ''),
                                'name_fa': fields.get('name_fa', ''),
                                'slug': fields.get('slug', ''),
                                'description_en': fields.get('description_en', ''),
                                'description_fa': fields.get('description_fa', ''),
                            }
                        )
                        imported_count += 1

                    messages.success(request, f'{imported_count} دسته‌بندی با موفقیت وارد شد')

                elif isinstance(data, dict) and 'categories' in data:
                    # فرمت قدیمی
                    categories = data.get('categories', [])

                    imported_count = 0
                    for cat in categories:
                        Category.objects.update_or_create(
                            pk=cat.get('id'),
                            defaults={
                                'name_en': cat.get('name_en', ''),
                                'name_fa': cat.get('name_fa', ''),
                                'slug': cat.get('slug', ''),
                                'description_en': cat.get('description_en', ''),
                                'description_fa': cat.get('description_fa', ''),
                            }
                        )
                        imported_count += 1

                    messages.success(request, f'{imported_count} دسته‌بندی با موفقیت وارد شد')

                else:
                    messages.error(request, 'فرمت فایل JSON معتبر نیست')

            except json.JSONDecodeError:
                messages.error(request, 'فایل JSON معتبر نیست')
            except Exception as e:
                messages.error(request, f'خطا در وارد کردن فایل: {str(e)}')

            return redirect('..')

        return render(request, 'admin/blog/category/import_json.html')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fa', 'author', 'category', 'published', 'created_at', 'views')
    list_filter = ('published', 'category', 'created_at')
    search_fields = ('title_en', 'title_fa', 'content_en', 'content_fa')
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ('created_at', 'updated_at', 'views')

    fieldsets = (
        ('English Content', {
            'fields': ('title_en', 'slug', 'content_en')
        }),
        ('Persian Content', {
            'fields': ('title_fa', 'content_fa')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'published', 'views', 'created_at', 'updated_at')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.import_json_view, name='blogpost_import_json'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def import_json_view(self, request):
        if request.method == 'POST':
            json_file = request.FILES.get('json_file')

            if not json_file:
                messages.error(request, 'لطفا یک فایل انتخاب کنید')
                return redirect('..')

            try:
                data = json.load(json_file)

                # بررسی فرمت fixture یا ساختار قدیمی
                if isinstance(data, list):
                    # فرمت Django fixture
                    posts = [item for item in data if item.get('model') == 'blog.blogpost']

                    imported_count = 0
                    for item in posts:
                        fields = item.get('fields', {})

                        # پیدا کردن category
                        category_id = fields.get('category')
                        try:
                            category = Category.objects.get(pk=category_id)
                        except Category.DoesNotExist:
                            messages.warning(request,
                                             f'دسته‌بندی با ID {category_id} یافت نشد. پست {item.get("pk")} وارد نشد.')
                            continue

                        # تنظیم author
                        author_id = fields.get('author')
                        if author_id:
                            from django.contrib.auth import get_user_model
                            User = get_user_model()
                            try:
                                author = User.objects.get(pk=author_id)
                            except User.DoesNotExist:
                                author = request.user
                        else:
                            author = request.user

                        BlogPost.objects.update_or_create(
                            pk=item.get('pk'),
                            defaults={
                                'title_en': fields.get('title_en', ''),
                                'title_fa': fields.get('title_fa', ''),
                                'slug': fields.get('slug', ''),
                                'content_en': fields.get('content_en', ''),
                                'content_fa': fields.get('content_fa', ''),
                                'author': author,
                                'category': category,
                                'published': fields.get('published', False),
                                'views': fields.get('views', 0),
                            }
                        )
                        imported_count += 1

                    messages.success(request, f'{imported_count} پست با موفقیت وارد شد')

                elif isinstance(data, dict) and 'posts' in data:
                    # فرمت قدیمی
                    posts = data.get('posts', [])

                    imported_count = 0
                    for post in posts:
                        # پیدا کردن category
                        category_id = post.get('category')
                        try:
                            category = Category.objects.get(pk=category_id)
                        except Category.DoesNotExist:
                            messages.warning(request,
                                             f'دسته‌بندی با ID {category_id} یافت نشد. پست "{post.get("title_en")}" وارد نشد.')
                            continue

                        # تنظیم author
                        author_id = post.get('author')
                        if author_id:
                            from django.contrib.auth import get_user_model
                            User = get_user_model()
                            try:
                                author = User.objects.get(pk=author_id)
                            except User.DoesNotExist:
                                author = request.user
                        else:
                            author = request.user

                        BlogPost.objects.update_or_create(
                            pk=post.get('id'),
                            defaults={
                                'title_en': post.get('title_en', ''),
                                'title_fa': post.get('title_fa', ''),
                                'slug': post.get('slug', ''),
                                'content_en': post.get('content_en', ''),
                                'content_fa': post.get('content_fa', ''),
                                'author': author,
                                'category': category,
                                'published': post.get('published', False),
                                'views': post.get('views', 0),
                            }
                        )
                        imported_count += 1

                    messages.success(request, f'{imported_count} پست با موفقیت وارد شد')

                else:
                    messages.error(request, 'فرمت فایل JSON معتبر نیست')

            except json.JSONDecodeError:
                messages.error(request, 'فایل JSON معتبر نیست')
            except Exception as e:
                messages.error(request, f'خطا در وارد کردن فایل: {str(e)}')

            return redirect('..')

        return render(request, 'admin/import_json.html')
