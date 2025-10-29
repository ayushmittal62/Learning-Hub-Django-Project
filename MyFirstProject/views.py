from django.shortcuts import redirect, render, get_object_or_404
from .models import SampleModel, SubjectReview, Student, Blog, BlogComment
from django.db.models import Avg, Count, Q
from .forms import LoginForm, ForgotPasswordForm, CustomSetPasswordForm, BlogForm, BlogCommentForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.
def all_html(request):
    # Get all subjects with review count and average rating
    Subjects = SampleModel.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating'),
        student_count=Count('students')
    ).all()
    return render(request, 'MyProject/all_html.html', {'Subjects': Subjects})

def subject_detail(request, subject_id):
    subject = get_object_or_404(SampleModel, pk=subject_id)
    
    # Get reviews for this subject (ordered by most recent)
    reviews = subject.reviews.select_related('user').order_by('-date_time')[:5]
    
    # Get enrolled students (ordered by name)
    enrolled_students = subject.students.order_by('name')[:10]
    
    # Calculate statistics
    review_count = subject.reviews.count()
    avg_rating = subject.reviews.aggregate(Avg('rating'))['rating__avg']
    student_count = subject.students.count()
    
    # Debug output
    print(f"\n=== DEBUG: Subject Detail ===")
    print(f"Subject: {subject.name}")
    print(f"Reviews count: {review_count}")
    print(f"Reviews: {list(reviews)}")
    print(f"Students count: {student_count}")
    print(f"Students: {list(enrolled_students)}")
    print(f"Average rating: {avg_rating}")
    print(f"===========================\n")
    
    context = {
        'subject': subject,
        'reviews': reviews,
        'enrolled_students': enrolled_students,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'student_count': student_count,
    }
    
    return render(request, 'MyProject/subject_detail.html', context)


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        elif hasattr(request.user, 'profile'):
            if request.user.profile.user_type == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        return redirect('all_html')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']

            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Automatically determine user type
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'profile') and user.profile.user_type == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'MyProject/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('user_login')


# Forgot Password Views
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Send email (for development, we'll just show the link)
            # In production, you should send actual email
            try:
                send_mail(
                    subject='Password Reset Request - Learning Hub',
                    message=f'Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset link has been sent to your email!')
            except Exception as e:
                # For development without email setup, show the link
                messages.success(request, f'Password reset link: {reset_link}')
                print(f"\n=== PASSWORD RESET LINK ===\n{reset_link}\n===========================\n")
            
            return redirect('user_login')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'MyProject/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Update session to prevent logout after password change
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
                
                messages.success(request, 'Your password has been reset successfully! You can now login.')
                return redirect('password_reset_complete')
            else:
                # Show form errors if validation fails
                messages.error(request, 'Please correct the errors below.')
        else:
            form = CustomSetPasswordForm(user)
        
        return render(request, 'MyProject/reset_password.html', {'form': form, 'validlink': True})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return render(request, 'MyProject/reset_password.html', {'form': None, 'validlink': False})


def password_reset_complete(request):
    return render(request, 'MyProject/password_reset_complete.html')


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    if not (hasattr(request.user, 'profile') and request.user.profile.user_type == 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('all_html')
    
    # Get statistics
    total_subjects = SampleModel.objects.count()
    total_students = Student.objects.count()
    total_reviews = SubjectReview.objects.count()
    
    # Get subjects with stats
    subjects = SampleModel.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating'),
        student_count=Count('students')
    ).all()
    
    # Get recent reviews
    recent_reviews = SubjectReview.objects.select_related('user', 'subject').order_by('-date_time')[:5]
    
    context = {
        'total_subjects': total_subjects,
        'total_students': total_students,
        'total_reviews': total_reviews,
        'subjects': subjects,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'MyProject/admin_dashboard.html', context)


def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    subjects = SampleModel.objects.all()
    return render(request, 'MyProject/user_dashboard.html', {'subjects': subjects})

# Helper function to check if user is superadmin
def is_superadmin(user):
    return user.is_superuser

# Public Blog Views (Anyone can view)
def blog_list(request):
    """Display all published blogs"""
    # Get search query
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Start with published blogs
    blogs = Blog.objects.filter(status='published')
    
    # Apply search filter
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        blogs = blogs.filter(category=category_filter)
    
    # Get categories for filter dropdown
    categories = Blog.CATEGORY_CHOICES
    
    # Annotate with comment count
    blogs = blogs.annotate(comment_count=Count('comments')).order_by('-published_at')
    
    context = {
        'blogs': blogs,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
        'total_blogs': blogs.count(),
    }
    
    return render(request, 'MyProject/blog_list.html', context)


def blog_detail(request, slug):
    """Display single blog post with comments"""
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    # Increment view count
    blog.views += 1
    blog.save(update_fields=['views'])
    
    # Get comments
    comments = blog.comments.select_related('user').all()
    
    # Handle comment form
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = BlogCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog_detail', slug=slug)
    else:
        comment_form = BlogCommentForm()
    
    # Get related blogs (same category, exclude current)
    related_blogs = Blog.objects.filter(
        category=blog.category,
        status='published'
    ).exclude(id=blog.id)[:3]
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'related_blogs': related_blogs,
        'reading_time': blog.get_reading_time(),
    }
    
    return render(request, 'MyProject/blog_detail.html', context)


# Superadmin Only Blog Views (CRUD Operations)
@login_required
@user_passes_test(is_superadmin, login_url='/login/')
def blog_create(request):
    """Create new blog post (Superadmin only)"""
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, f'Blog "{blog.title}" created successfully!')
            return redirect('blog_manage')
    else:
        form = BlogForm()
    
    return render(request, 'MyProject/blog_form.html', {
        'form': form,
        'title': 'Create New Blog Post',
        'button_text': 'Create Blog'
    })


@login_required
@user_passes_test(is_superadmin, login_url='/login/')
def blog_update(request, slug):
    """Update existing blog post (Superadmin only)"""
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f'Blog "{blog.title}" updated successfully!')
            return redirect('blog_manage')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'MyProject/blog_form.html', {
        'form': form,
        'title': f'Edit: {blog.title}',
        'button_text': 'Update Blog',
        'blog': blog
    })


@login_required
@user_passes_test(is_superadmin, login_url='/login/')
def blog_delete(request, slug):
    """Delete blog post (Superadmin only)"""
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.method == 'POST':
        title = blog.title
        blog.delete()
        messages.success(request, f'Blog "{title}" deleted successfully!')
        return redirect('blog_manage')
    
    return render(request, 'MyProject/blog_delete.html', {'blog': blog})


@login_required
@user_passes_test(is_superadmin, login_url='/login/')
def blog_manage(request):
    """Manage all blogs (Superadmin only) - Dashboard"""
    # Get all blogs (including drafts)
    blogs = Blog.objects.annotate(
        comment_count=Count('comments')
    ).order_by('-created_at')
    
    # Statistics
    total_blogs = blogs.count()
    published_blogs = blogs.filter(status='published').count()
    draft_blogs = blogs.filter(status='draft').count()
    total_views = sum(blog.views for blog in blogs)
    
    context = {
        'blogs': blogs,
        'total_blogs': total_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'total_views': total_views,
    }
    
    return render(request, 'MyProject/blog_manage.html', context)

