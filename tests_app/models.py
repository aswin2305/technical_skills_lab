from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from questions.models import Question
from candidates.models import Candidate, CandidateGroup


class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    candidate_group = models.ForeignKey(CandidateGroup, on_delete=models.CASCADE, related_name='tests')
    questions = models.ManyToManyField(Question, through='TestQuestion')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(help_text="Time limit once a student starts")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def total_marks(self):
        return sum(tq.marks for tq in self.testquestion_set.all())

    @property
    def is_active_window(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.test.title} - {self.question.title}"


class Assignment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='assignments')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='assignments')
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    total_score = models.FloatField(default=0)
    max_score = models.FloatField(default=0)

    class Meta:
        unique_together = ('test', 'candidate')

    def __str__(self):
        return f"{self.candidate.name} - {self.test.title}"

    @property
    def deadline(self):
        if not self.started_at:
            return self.test.end_time
        from datetime import timedelta
        by_duration = self.started_at + timedelta(minutes=self.test.duration_minutes)
        return min(by_duration, self.test.end_time)

    @property
    def status(self):
        now = timezone.now()
        if self.is_completed:
            return 'completed'
        if now < self.test.start_time:
            return 'upcoming'
        if now > self.test.end_time:
            return 'missed'
        return 'ongoing'


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField(blank=True)
    score = models.FloatField(default=0)
    max_score = models.FloatField(default=0)
    test_case_results = models.JSONField(default=dict, blank=True)
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'question')

    def __str__(self):
        return f"{self.assignment.candidate.name} - {self.question.title}"