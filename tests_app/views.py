from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from candidates.decorators import admin_required
from .models import Test, TestQuestion, Assignment, Submission
from .forms import AssignTestForm
from candidates.models import Candidate
from grading.grader import grade_code
import openpyxl


# ---------- ADMIN VIEWS ----------

@login_required
@admin_required
def admin_dashboard(request):
    context = {
        'total_students': Candidate.objects.count(),
        'total_tests': Test.objects.count(),
        'total_submissions': Submission.objects.count(),
        'recent_tests': Test.objects.order_by('-created_at')[:5],
    }
    return render(request, 'tests_app/admin_dashboard.html', context)


@login_required
@admin_required
def assign_test(request):
    if request.method == 'POST':
        form = AssignTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()

            selected_questions = form.cleaned_data['questions']
            for q in selected_questions:
                TestQuestion.objects.create(test=test, question=q, marks=q.marks)

            candidates = Candidate.objects.filter(group=test.candidate_group)
            for c in candidates:
                Assignment.objects.get_or_create(test=test, candidate=c)

            messages.success(request, f"Test '{test.title}' assigned to {candidates.count()} candidate(s).")
            return redirect('manage_tests')
    else:
        form = AssignTestForm()
    return render(request, 'tests_app/assign_test.html', {'form': form})


@login_required
@admin_required
def manage_tests(request):
    tests = Test.objects.all().order_by('-created_at')
    return render(request, 'tests_app/manage_tests.html', {'tests': tests})


@login_required
@admin_required
def view_report(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    assignments = test.assignments.select_related('candidate').all().order_by('-total_score')
    return render(request, 'tests_app/view_report.html', {'test': test, 'assignments': assignments})


@login_required
@admin_required
def export_report_excel(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    assignments = test.assignments.select_related('candidate').all().order_by('-total_score')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(['Name', 'Username', 'Department', 'Group', 'Status', 'Score', 'Max Score'])

    for a in assignments:
        ws.append([
            a.candidate.name,
            a.candidate.user.username,
            a.candidate.department,
            a.candidate.group.name if a.candidate.group else '',
            a.status,
            a.total_score,
            a.max_score,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{test.title}_report.xlsx"'
    wb.save(response)
    return response


# ---------- STUDENT VIEWS ----------

@login_required
def student_dashboard(request):
    candidate = get_object_or_404(Candidate, user=request.user)
    assignments = Assignment.objects.filter(candidate=candidate).select_related('test').order_by('-test__start_time')
    return render(request, 'tests_app/student_dashboard.html', {'assignments': assignments})


@login_required
def start_test(request, assignment_id):
    candidate = get_object_or_404(Candidate, user=request.user)
    assignment = get_object_or_404(Assignment, pk=assignment_id, candidate=candidate)

    if assignment.is_completed:
        return redirect('test_result', assignment_id=assignment.id)

    now = timezone.now()
    if now < assignment.test.start_time or now > assignment.test.end_time:
        messages.error(request, "This test is not currently available.")
        return redirect('student_dashboard')

    if not assignment.started_at:
        assignment.started_at = now
        assignment.save()

    return redirect('take_test', assignment_id=assignment.id)


@login_required
def take_test(request, assignment_id):
    candidate = get_object_or_404(Candidate, user=request.user)
    assignment = get_object_or_404(Assignment, pk=assignment_id, candidate=candidate)

    if assignment.is_completed:
        return redirect('test_result', assignment_id=assignment.id)

    now = timezone.now()
    if now > assignment.deadline:
        finalize_assignment(assignment)
        return redirect('test_result', assignment_id=assignment.id)

    test_questions = assignment.test.testquestion_set.select_related('question').all()

    if request.method == 'POST':
        for tq in test_questions:
            code = request.POST.get(f'code_{tq.question.id}', '')
            Submission.objects.update_or_create(
                assignment=assignment,
                question=tq.question,
                defaults={'code': code}
            )
        finalize_assignment(assignment)
        return redirect('test_result', assignment_id=assignment.id)

    # Pre-fill any previously saved code (resume)
    existing = {s.question_id: s.code for s in assignment.submissions.all()}

    context = {
        'assignment': assignment,
        'test_questions': test_questions,
        'existing': existing,
        'deadline_iso': assignment.deadline.isoformat(),
    }
    return render(request, 'tests_app/take_test.html', context)


def finalize_assignment(assignment):
    test_questions = assignment.test.testquestion_set.select_related('question').all()
    total_score = 0
    max_score = 0

    for tq in test_questions:
        submission, _ = Submission.objects.get_or_create(assignment=assignment, question=tq.question)
        score, q_max, results = grade_code(tq.question, submission.code)
        # scale score to the test's marks for this question
        scaled_score = round((score / q_max) * tq.marks, 2) if q_max > 0 else 0
        submission.score = scaled_score
        submission.max_score = tq.marks
        submission.test_case_results = results
        submission.save()

        total_score += scaled_score
        max_score += tq.marks

    assignment.total_score = total_score
    assignment.max_score = max_score
    assignment.is_completed = True
    assignment.submitted_at = timezone.now()
    assignment.save()


@login_required
def test_result(request, assignment_id):
    candidate = get_object_or_404(Candidate, user=request.user)
    assignment = get_object_or_404(Assignment, pk=assignment_id, candidate=candidate)
    submissions = assignment.submissions.select_related('question').all()
    return render(request, 'tests_app/test_result.html', {
        'assignment': assignment,
        'submissions': submissions
    })


@login_required
@admin_required
def edit_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        form = AssignTestForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.save()

            # Update the linked questions/marks
            TestQuestion.objects.filter(test=test).delete()
            selected_questions = form.cleaned_data['questions']
            for q in selected_questions:
                TestQuestion.objects.create(test=test, question=q, marks=q.marks)

            messages.success(request, f"Test '{test.title}' updated successfully.")
            return redirect('manage_tests')
    else:
        initial_questions = test.questions.all()
        form = AssignTestForm(instance=test, initial={'questions': initial_questions})
    return render(request, 'tests_app/edit_test.html', {'form': form, 'test': test})


@login_required
@admin_required
def delete_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    title = test.title
    test.delete()
    messages.success(request, f"Test '{title}' deleted.")
    return redirect('manage_tests')