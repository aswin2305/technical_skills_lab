from django.db import models
from django.contrib.auth.models import User

class CandidateGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_candidates(self):
        return self.candidates.count()


class Candidate(models.Model):
    YEAR_CHOICES = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )

    PROGRAM_LEVEL_CHOICES = (
        ('UG', 'Undergraduate (UG)'),
        ('PG', 'Postgraduate (PG)'),
    )

    DEGREE_CHOICES = (
        ('B.E.', 'Bachelor of Engineering (B.E.)'),
        ('B.Tech.', 'Bachelor of Technology (B.Tech.)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate')
    name = models.CharField(max_length=150)
    institution = models.CharField(max_length=200, default="IFET College of Engineering")
    program_level = models.CharField(max_length=2, choices=PROGRAM_LEVEL_CHOICES, default='UG')
    degree = models.CharField(max_length=100, default='B.E.',
                               help_text="Select a common degree or type your own")
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    batch_from = models.PositiveIntegerField()
    batch_to = models.PositiveIntegerField()
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    group = models.ForeignKey(CandidateGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def batch_display(self):
        return f"{self.batch_from} - {self.batch_to}"