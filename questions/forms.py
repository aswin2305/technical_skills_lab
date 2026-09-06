from django import forms
from django.forms import inlineformset_factory
from .models import Question, TestCase


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'language', 'prompt', 'reference_solution', 'marks',
                  'sql_setup_script', 'sql_reference_query']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control tsl-input', 'placeholder': 'Question title'}),
            'language': forms.Select(attrs={'class': 'form-select tsl-input', 'id': 'id_language'}),
            'prompt': forms.Textarea(attrs={'class': 'form-control tsl-input', 'rows': 5,
                                             'placeholder': 'Describe the problem statement...'}),
            'reference_solution': forms.Textarea(attrs={'class': 'form-control tsl-input mono', 'rows': 8,
                                                          'placeholder': 'Correct reference solution code'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control tsl-input'}),
            'sql_setup_script': forms.Textarea(attrs={'class': 'form-control tsl-input mono', 'rows': 4,
                                                        'placeholder': 'CREATE TABLE ... (SQL questions only)'}),
            'sql_reference_query': forms.Textarea(attrs={'class': 'form-control tsl-input mono', 'rows': 3,
                                                           'placeholder': 'SELECT ... (SQL questions only)'}),
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output', 'is_hidden']
        widgets = {
            'input_data': forms.Textarea(attrs={'class': 'form-control tsl-input mono', 'rows': 2,
                                                 'placeholder': 'Input (stdin) — leave blank if none'}),
            'expected_output': forms.Textarea(attrs={'class': 'form-control tsl-input mono', 'rows': 2,
                                                       'placeholder': 'Expected output'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'input_data': '',
            'expected_output': '',
        }


TestCaseFormSet = inlineformset_factory(
    Question, TestCase,
    form=TestCaseForm,
    extra=1,
    can_delete=True
)