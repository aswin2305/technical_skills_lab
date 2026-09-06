from django.contrib import admin
from .models import Test, TestQuestion, Assignment, Submission

class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'candidate_group', 'start_time', 'end_time', 'duration_minutes')
    inlines = [TestQuestionInline]

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'test', 'status', 'total_score', 'max_score')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'question', 'score', 'max_score')