from .judge0_client import run_code_judge0
from .sql_grader import run_sql_comparison


def grade_code(question, code):
    max_score = question.marks

    if question.language == 'sql':
        return grade_sql_question(question, code)

    test_cases = question.test_cases.all()
    total = len(test_cases)
    passed_count = 0
    results = []

    for tc in test_cases:
        actual = run_code_judge0(code, question.language, tc.input_data)
        expected = tc.expected_output.strip()

        actual_normalized = actual.strip().lower()
        expected_normalized = expected.lower()
        passed = (actual_normalized == expected_normalized)

        if passed:
            passed_count += 1

        results.append({
            'input': tc.input_data if not tc.is_hidden else '(hidden)',
            'expected': expected if not tc.is_hidden else '(hidden)',
            'actual': actual if not tc.is_hidden else ('(hidden)' if passed else actual),
            'passed': passed
        })

    score = round((passed_count / total) * max_score, 2) if total > 0 else 0
    return score, max_score, results


def grade_sql_question(question, student_query):
    max_score = question.marks

    if not question.sql_setup_script or not question.sql_reference_query:
        return 0, max_score, [{
            'input': '(SQL setup missing)',
            'expected': '',
            'actual': '',
            'passed': False
        }]

    passed, student_result, reference_result, error = run_sql_comparison(
        question.sql_setup_script,
        student_query,
        question.sql_reference_query
    )

    score = max_score if passed else 0

    result_entry = {
        'input': '(SQL setup script applied)',
        'expected': str(reference_result) if reference_result is not None else '(error)',
        'actual': str(student_result) if student_result is not None else (error or '(error)'),
        'passed': passed
    }

    return score, max_score, [result_entry]