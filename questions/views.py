from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from candidates.decorators import admin_required
from .models import Question
from .forms import QuestionForm, TestCaseFormSet


@login_required
@admin_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()

            formset = TestCaseFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                messages.success(request, f"Question '{question.title}' created successfully.")
                return redirect('manage_questions')
            else:
                question.delete()
                messages.error(request, "Please fix the test case errors below.")
        else:
            formset = TestCaseFormSet(request.POST)
    else:
        form = QuestionForm()
        formset = TestCaseFormSet()

    return render(request, 'questions/create_question.html', {'form': form, 'formset': formset})


@login_required
@admin_required
def manage_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions/manage_questions.html', {'questions': questions})


@login_required
@admin_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = TestCaseFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Question updated successfully.")
            return redirect('manage_questions')
    else:
        form = QuestionForm(instance=question)
        formset = TestCaseFormSet(instance=question)

    return render(request, 'questions/edit_question.html', {
        'form': form, 'formset': formset, 'question': question
    })


@login_required
@admin_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.usage_count > 0:
        messages.error(request, "Cannot delete — this question is used in one or more tests.")
        return redirect('manage_questions')
    title = question.title
    question.delete()
    messages.success(request, f"Question '{title}' deleted.")
    return redirect('manage_questions')