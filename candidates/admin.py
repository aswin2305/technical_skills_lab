from django.contrib import admin
from .models import Candidate, CandidateGroup

@admin.register(CandidateGroup)
class CandidateGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'total_candidates', 'created_at')
    search_fields = ('name', 'department')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'institution', 'program_level', 'degree', 'department', 'year', 'batch_display', 'group', 'email')
    list_filter = ('institution', 'program_level', 'degree', 'department', 'year', 'group')
    search_fields = ('name', 'user__username', 'email')