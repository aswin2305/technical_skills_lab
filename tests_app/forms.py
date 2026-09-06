from django import forms
from .models import Test
from candidates.models import CandidateGroup
from questions.models import Question


class AssignTestForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Test
        fields = ['title', 'description', 'candidate_group', 'start_time', 'end_time', 'duration_minutes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control tsl-input', 'rows': 3}),
            'candidate_group': forms.Select(attrs={'class': 'form-select tsl-input'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control tsl-input', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control tsl-input', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control tsl-input'}),
        }