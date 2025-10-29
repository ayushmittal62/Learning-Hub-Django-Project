from django.contrib import admin
from .models import SampleModel, SubjectReview, Student, StudentProfile, UserProfile, Blog, BlogComment

class SubjectReviewInline(admin.TabularInline):
    model = SubjectReview
    extra = 1
    readonly_fields = ['date_time']

@admin.register(SampleModel)
class SampleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'date_time', 'get_review_count']
    list_filter = ['type', 'date_time']
    search_fields = ['name', 'description']
    readonly_fields = ['date_time']
    inlines = [SubjectReviewInline]
    
    def get_review_count(self, obj):
        return obj.reviews.count()
    get_review_count.short_description = 'Reviews'

@admin.register(SubjectReview)
class SubjectReviewAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'rating', 'date_time']
    list_filter = ['rating', 'date_time']
    search_fields = ['subject__name', 'user__username', 'comment']
    readonly_fields = ['date_time']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'get_enrolled_count']
    search_fields = ['name', 'location']
    filter_horizontal = ['enrolled_courses']
    
    def get_enrolled_count(self, obj):
        return obj.enrolled_courses.count()
    get_enrolled_count.short_description = 'Enrolled Courses'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student', 'profile_number', 'time_created']
    search_fields = ['student__name', 'profile_number']
    readonly_fields = ['time_created']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at', 'published_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
        ('Metadata', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'comment_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment', 'user__username', 'blog__title']
    readonly_fields = ['created_at']
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment'