from django.contrib import admin
from .models import SampleModel, SubjectReview, Student, StudentProfile, UserProfile

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
