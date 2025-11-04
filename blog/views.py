from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from .models import BlogPost, Category


def blog_list(request):
    """Blog list page with pagination and search"""
    language = get_language()
    posts = BlogPost.objects.filter(published=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title_en__icontains=search_query) |
            Q(title_fa__icontains=search_query) |
            Q(content_en__icontains=search_query) |
            Q(content_fa__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'search_query': search_query,
        'language': language,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Blog post detail page"""
    language = get_language()
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    
    # Increment views
    post.increment_views()
    
    # Related posts
    related_posts = BlogPost.objects.filter(
        category=post.category,
        published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'language': language,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_category(request, slug):
    """Blog posts filtered by category"""
    language = get_language()
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, published=True)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'language': language,
    }
    return render(request, 'blog/blog_category.html', context)
