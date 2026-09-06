from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import StudentLoginForm, AdminLoginForm, TSLPasswordChangeForm


def login_student(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if hasattr(user, 'profile') and user.profile.role == 'student':
                    login(request, user)
                    request.session['role'] = 'student'
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "This login is for students only.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = StudentLoginForm()
    return render(request, 'accounts/login_student.html', {'form': form})


def login_admin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if hasattr(user, 'profile') and user.profile.role == 'admin':
                    login(request, user)
                    request.session['role'] = 'admin'
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "This login is for administrators only.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/login_admin.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


class TSLPasswordChangeView(PasswordChangeView):
    form_class = TSLPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)