from django import forms
from django.contrib.auth.models import User
from .models import Candidate, CandidateGroup


class CandidateCreateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control tsl-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control tsl-input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control tsl-input'}))

    class Meta:
        model = Candidate
        fields = ['name', 'institution', 'program_level', 'degree', 'department', 'year',
                  'batch_from', 'batch_to', 'email', 'mobile_number', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'institution': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'program_level': forms.Select(attrs={'class': 'form-select tsl-input'}),
            'degree': forms.TextInput(attrs={
                'class': 'form-control tsl-input',
                'list': 'degree-options',
                'placeholder': 'e.g. B.E. or type your own'
            }),
            'department': forms.TextInput(attrs={'class': 'form-control tsl-input', 'placeholder': 'e.g. Computer Science and Engineering (CSE)'}),
            'year': forms.Select(attrs={'class': 'form-select tsl-input'}),
            'batch_from': forms.NumberInput(attrs={'class': 'form-control tsl-input', 'placeholder': 'e.g. 2023'}),
            'batch_to': forms.NumberInput(attrs={'class': 'form-control tsl-input', 'placeholder': 'e.g. 2027'}),
            'email': forms.EmailInput(attrs={'class': 'form-control tsl-input'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'group': forms.Select(attrs={'class': 'form-select tsl-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        batch_from = cleaned_data.get('batch_from')
        batch_to = cleaned_data.get('batch_to')
        if batch_from and batch_to and batch_from > batch_to:
            raise forms.ValidationError("Batch 'From' year cannot be after 'To' year.")
        return cleaned_data


class CandidateEditForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'institution', 'program_level', 'degree', 'department', 'year',
                  'batch_from', 'batch_to', 'email', 'mobile_number', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'institution': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'program_level': forms.Select(attrs={'class': 'form-select tsl-input'}),
            'degree': forms.TextInput(attrs={
                'class': 'form-control tsl-input',
                'list': 'degree-options',
            }),
            'department': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'year': forms.Select(attrs={'class': 'form-select tsl-input'}),
            'batch_from': forms.NumberInput(attrs={'class': 'form-control tsl-input'}),
            'batch_to': forms.NumberInput(attrs={'class': 'form-control tsl-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control tsl-input'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'group': forms.Select(attrs={'class': 'form-select tsl-input'}),
        }


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control tsl-input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control tsl-input'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class CandidateGroupForm(forms.ModelForm):
    class Meta:
        model = CandidateGroup
        fields = ['name', 'department', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control tsl-input', 'placeholder': 'e.g. CSE 2024 Batch'}),
            'department': forms.TextInput(attrs={'class': 'form-control tsl-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control tsl-input', 'rows': 3}),
        }