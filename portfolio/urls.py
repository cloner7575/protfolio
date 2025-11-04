from django.urls import path
from . import views
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('experience/', views.experience, name='experience'),
    path('education/', views.education, name='education'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
]

# Test error pages (only in DEBUG mode - remove in production)
if settings.DEBUG:
    urlpatterns += [
        path('test-404/', TemplateView.as_view(template_name='404.html')),
        path('test-500/', TemplateView.as_view(template_name='500.html')),
    ]
