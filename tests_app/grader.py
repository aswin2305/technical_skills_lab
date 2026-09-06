import subprocess


def run_python(code, input_data, timeout=5):
    try:
        result = subprocess.run(
            ['python3', '-c', code],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"
    except Exception as e:
        return f"__ERROR__: {e}"


def grade_code(question, code):
    """
    Returns (score, max_score, results_list)
    results_list: [{input, expected, actual, passed}, ...]
    """
    test_cases = question.test_cases.all()
    total = len(test_cases)
    passed_count = 0
    results = []

    for tc in test_cases:
        if question.language == 'python':
            actual = run_python(code, tc.input_data)
        else:
            # Placeholder until Judge0 (C/C++/Java) and SQL sandbox are wired in next module
            actual = "__PENDING_GRADING_ENGINE__"

        expected = tc.expected_output.strip()
        passed = (actual == expected)
        if passed:
            passed_count += 1

        results.append({
            'input': tc.input_data if not tc.is_hidden else '(hidden)',
            'expected': expected if not tc.is_hidden else '(hidden)',
            'actual': actual if not tc.is_hidden else ('(hidden)' if passed else actual),
            'passed': passed
        })

    max_score = question.marks
    score = round((passed_count / total) * max_score, 2) if total > 0 else 0
    return score, max_score, results