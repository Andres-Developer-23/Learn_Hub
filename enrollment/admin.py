from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student, Course, CourseContent, Exam, Question, QuestionOption, ExamAttempt, CourseFile, EnrollmentRequest, Instructor

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'level', 'status', 'created_at')
    list_filter  = ('level', 'status')
    search_fields = ('name', 'email')
    ordering      = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'duration', 'is_active', 'order')
    list_filter  = ('level', 'is_active')
    search_fields = ('title',)

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('course', 'section_type', 'title', 'order')
    list_filter  = ('section_type',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'passing_score', 'time_limit_minutes')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text', 'order')
    search_fields = ('text',)

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'order')
    list_filter  = ('is_correct',)

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'total', 'passed', 'started_at')

@admin.register(CourseFile)
class CourseFileAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'uploaded_at')

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'created_at')
    list_filter = ('status', 'course', 'created_at')
    search_fields = ('student__name', 'student__email', 'course__title')
    ordering = ('-created_at',)
    raw_id_fields = ('student', 'course')


class InstructorInline(admin.StackedInline):
    model = Instructor
    can_delete = False
    verbose_name = 'Perfil de instructor'
    verbose_name_plural = 'Instructores'
    fields = ('name', 'email', 'bio', 'avatar_url')


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (InstructorInline,)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user_link', 'created_at')
    search_fields = ('name', 'email', 'user__username')
    raw_id_fields = ('user',)

    def user_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.user_id, obj.user.username)
    user_link.short_description = 'Usuario'
