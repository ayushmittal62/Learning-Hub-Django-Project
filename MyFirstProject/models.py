from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class SampleModel(models.Model):
    """Main Subject/Course Model"""
    STUDY_CHOICE = [
        ('AI', 'Artificial Intelligence'),
        ('DS', 'Data Science'),
        ('WD', 'Web Development'),
    ]
    name = models.CharField(max_length=100, verbose_name="Subject Name")
    image = models.ImageField(upload_to='images/', verbose_name="Subject Image")
    date_time = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    type = models.CharField(
        max_length=2, 
        choices=STUDY_CHOICE, 
        default='AI',
        verbose_name="Subject Type"
    )
    description = models.TextField(blank=True, default='', verbose_name="Description")

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['-date_time']

    def __str__(self):
        return self.name
    

# One-to-Many Relationship (Many Reviews for One Subject)
class SubjectReview(models.Model):
    """Review model - One Subject can have Many Reviews"""
    subject = models.ForeignKey(
        SampleModel, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name="Subject"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='subject_reviews',
        verbose_name="Reviewer"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating (1-5)"
    )
    comment = models.TextField(verbose_name="Review Comment")
    date_time = models.DateTimeField(default=timezone.now, verbose_name="Review Date")

    class Meta:
        verbose_name = "Subject Review"
        verbose_name_plural = "Subject Reviews"
        ordering = ['-date_time']
        unique_together = ['subject', 'user']  # One user can only review a subject once

    def __str__(self):
        return f'{self.subject.name} - {self.rating}★ by {self.user.username}'
    

# Many-to-Many Relationship (Students can enroll in Many Subjects, Subjects can have Many Students)
class Student(models.Model):
    """Student model - Many-to-Many with Subjects"""
    name = models.CharField(max_length=100, verbose_name="Student Name")
    location = models.CharField(max_length=100, verbose_name="Location")
    enrolled_courses = models.ManyToManyField(
        SampleModel, 
        related_name='students',
        blank=True,
        verbose_name="Enrolled Courses"
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_enrolled_count(self):
        """Returns the number of courses the student is enrolled in"""
        return self.enrolled_courses.count()
    

# One-to-One Relationship (Each Student has One Profile)
class StudentProfile(models.Model):
    """Student Profile - One-to-One with Student"""
    student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="Student"
    )
    bio = models.TextField(blank=True, verbose_name="Biography")
    profile_number = models.IntegerField(unique=True, verbose_name="Profile Number")
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        verbose_name="Profile Picture"
    )
    time_created = models.DateTimeField(default=timezone.now, verbose_name="Profile Created")

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
        ordering = ['-time_created']

    def __str__(self):
        return f'Profile of {self.student.name}'
    

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# Signal to automatically create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance, user_type='user')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser and hasattr(instance, 'profile'):
        instance.profile.save()


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('education', 'Education'),
        ('programming', 'Programming'),
        ('data-science', 'Data Science'),
        ('web-development', 'Web Development'),
        ('ai-ml', 'AI & Machine Learning'),
        ('career', 'Career'),
        ('tips', 'Tips & Tricks'),
    ]


    title = models.CharField(max_length=200, verbose_name="Blog Title")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL Slug")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', verbose_name="Author")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='technology', verbose_name="Category")
    content = models.TextField(verbose_name="Blog Content")
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary (max 300 characters)")
    featured_image = models.URLField(max_length=500, blank=True, help_text="URL of the featured image")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def reading_time(self):
        word_count = len(self.content.split())
        reading_speed_wpm = 200 
        return max(1, word_count // reading_speed_wpm)
    
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} on {self.blog.title}"