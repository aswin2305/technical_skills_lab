import sqlite3


def run_sql_comparison(setup_script, student_query, reference_query, timeout=5):
    try:
        ref_conn = sqlite3.connect(":memory:")
        ref_cursor = ref_conn.cursor()
        ref_cursor.executescript(setup_script)
        ref_cursor.execute(reference_query)
        reference_result = ref_cursor.fetchall()
        ref_conn.close()
    except Exception as e:
        return False, None, None, f"Reference query error: {e}"

    try:
        student_conn = sqlite3.connect(":memory:")
        student_cursor = student_conn.cursor()
        student_cursor.executescript(setup_script)
        student_cursor.execute(student_query)
        student_result = student_cursor.fetchall()
        student_conn.close()
    except Exception as e:
        return False, None, reference_result, f"Student query error: {e}"

    passed = sorted(student_result) == sorted(reference_result)
    return passed, student_result, reference_result, None