from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from .models import Candidate, CandidateGroup
from .forms import CandidateCreateForm, CandidateEditForm, ResetPasswordForm, CandidateGroupForm
from accounts.models import Profile


@login_required
@admin_required
def create_candidate(request):
    if request.method == 'POST':
        form = CandidateCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data['email']
            )
            Profile.objects.create(user=user, role='student')

            candidate = form.save(commit=False)
            candidate.user = user
            candidate.save()

            messages.success(request, f"Candidate '{candidate.name}' created successfully.")
            return redirect('manage_candidates')
    else:
        form = CandidateCreateForm()
    return render(request, 'candidates/create_candidate.html', {'form': form})


@login_required
@admin_required
def manage_candidates(request):
    candidates = Candidate.objects.select_related('user', 'group').all().order_by('-created_at')
    return render(request, 'candidates/manage_candidates.html', {'candidates': candidates})


@login_required
@admin_required
def edit_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateEditForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            candidate.user.email = form.cleaned_data['email']
            candidate.user.save()
            messages.success(request, "Candidate details updated.")
            return redirect('manage_candidates')
    else:
        form = CandidateEditForm(instance=candidate)
    return render(request, 'candidates/edit_candidate.html', {'form': form, 'candidate': candidate})


@login_required
@admin_required
def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    user = candidate.user
    name = candidate.name
    candidate.delete()
    user.delete()
    messages.success(request, f"Candidate '{name}' deleted.")
    return redirect('manage_candidates')


@login_required
@admin_required
def reset_password(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            candidate.user.set_password(form.cleaned_data['new_password'])
            candidate.user.save()
            messages.success(request, f"Password reset for '{candidate.name}'.")
            return redirect('manage_candidates')
    else:
        form = ResetPasswordForm()
    return render(request, 'candidates/reset_password.html', {'form': form, 'candidate': candidate})


@login_required
@admin_required
def create_group(request):
    if request.method == 'POST':
        form = CandidateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate group created.")
            return redirect('manage_groups')
    else:
        form = CandidateGroupForm()
    return render(request, 'candidates/create_group.html', {'form': form})


@login_required
@admin_required
def manage_groups(request):
    groups = CandidateGroup.objects.all().order_by('-created_at')
    return render(request, 'candidates/manage_groups.html', {'groups': groups})


@login_required
@admin_required
def edit_group(request, pk):
    group = get_object_or_404(CandidateGroup, pk=pk)
    if request.method == 'POST':
        form = CandidateGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated.")
            return redirect('manage_groups')
    else:
        form = CandidateGroupForm(instance=group)
    return render(request, 'candidates/edit_group.html', {'form': form, 'group': group})


@login_required
@admin_required
def delete_group(request, pk):
    group = get_object_or_404(CandidateGroup, pk=pk)
    group.delete()
    messages.success(request, "Group deleted.")
    return redirect('manage_groups')