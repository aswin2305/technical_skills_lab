from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    LANGUAGE_CHOICES = (
        ('c', 'C'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('python', 'Python'),
        ('sql', 'SQL'),
    )

    title = models.CharField(max_length=200)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    prompt = models.TextField(help_text="The problem statement shown to students")
    reference_solution = models.TextField(help_text="Correct solution code used for reference")
    marks = models.PositiveIntegerField(default=10)

    # SQL-specific fields (used only when language == 'sql')
    sql_setup_script = models.TextField(blank=True, null=True,
                                         help_text="SQL to create/seed tables (SQL questions only)")
    sql_reference_query = models.TextField(blank=True, null=True,
                                            help_text="Correct SQL query (SQL questions only)")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"

    @property
    def usage_count(self):
        return self.testquestion_set.count()


class TestCase(models.Model):
    question = models.ForeignKey(Question, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.TextField(blank=True, help_text="Input passed to the program (stdin)")
    expected_output = models.TextField(help_text="Expected output to match against")
    is_hidden = models.BooleanField(default=False, help_text="Hide this test case's details from students")

    def __str__(self):
        return f"TestCase #{self.id} for {self.question.title}"