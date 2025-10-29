from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_html, name='all_html'),
    path('<int:subject_id>/', views.subject_detail, name='subject_detail'),
    
    # Authentication URLs
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Password Reset URLs
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
    
    # Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    # Blog URLs - Superadmin CRUD (MUST come BEFORE blog detail)
    path('blogs/manage/', views.blog_manage, name='blog_manage'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/<slug:slug>/edit/', views.blog_update, name='blog_update'),
    path('blogs/<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
    
    # Blog URLs - Public (MUST come AFTER specific URLs)
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
