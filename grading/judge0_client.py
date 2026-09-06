import subprocess
import tempfile
import os
import uuid
import sys


def run_code_judge0(source_code, language, stdin_data, timeout=10):
    """
    Runs code locally using installed compilers/interpreters.
    Function name kept as 'run_code_judge0' so grader.py doesn't need changes.
    """
    unique_id = str(uuid.uuid4())[:8]
    temp_dir = tempfile.mkdtemp(prefix=f"tsl_{unique_id}_")

    try:
        if language == 'python':
            return _run_python(source_code, stdin_data, temp_dir, timeout)
        elif language == 'c':
            return _run_c(source_code, stdin_data, temp_dir, timeout)
        elif language == 'cpp':
            return _run_cpp(source_code, stdin_data, temp_dir, timeout)
        elif language == 'java':
            return _run_java(source_code, stdin_data, temp_dir, timeout)
        else:
            return f"__ERROR__: Unsupported language '{language}'"
    finally:
        _cleanup(temp_dir)


def _cleanup(temp_dir):
    try:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except Exception:
        pass



def _run_python(code, stdin_data, temp_dir, timeout):
    file_path = os.path.join(temp_dir, "script.py")
    with open(file_path, "w") as f:
        f.write(code)

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            return f"__ERROR__: {result.stderr.strip()}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"
    except Exception as e:
        return f"__ERROR__: {e}"



def _run_c(code, stdin_data, temp_dir, timeout):
    source_path = os.path.join(temp_dir, "main.c")
    exe_path = os.path.join(temp_dir, "main.exe")
    with open(source_path, "w") as f:
        f.write(code)

    compile_result = subprocess.run(
        ["gcc", source_path, "-o", exe_path],
        capture_output=True, text=True, timeout=timeout
    )
    if compile_result.returncode != 0:
        return f"__ERROR__: Compile error - {compile_result.stderr.strip()}"

    try:
        run_result = subprocess.run(
            [exe_path],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if run_result.returncode != 0:
            return f"__ERROR__: {run_result.stderr.strip()}"
        return run_result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"
    except Exception as e:
        return f"__ERROR__: {e}"


def _run_cpp(code, stdin_data, temp_dir, timeout):
    source_path = os.path.join(temp_dir, "main.cpp")
    exe_path = os.path.join(temp_dir, "main.exe")
    with open(source_path, "w") as f:
        f.write(code)

    compile_result = subprocess.run(
        ["g++", source_path, "-o", exe_path],
        capture_output=True, text=True, timeout=timeout
    )
    if compile_result.returncode != 0:
        return f"__ERROR__: Compile error - {compile_result.stderr.strip()}"

    try:
        run_result = subprocess.run(
            [exe_path],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if run_result.returncode != 0:
            return f"__ERROR__: {run_result.stderr.strip()}"
        return run_result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"
    except Exception as e:
        return f"__ERROR__: {e}"


def _run_java(code, stdin_data, temp_dir, timeout):
    source_path = os.path.join(temp_dir, "Main.java")
    with open(source_path, "w") as f:
        f.write(code)

    compile_result = subprocess.run(
        ["javac", source_path],
        capture_output=True, text=True, timeout=timeout, cwd=temp_dir
    )
    if compile_result.returncode != 0:
        return f"__ERROR__: Compile error - {compile_result.stderr.strip()}"

    try:
        run_result = subprocess.run(
            ["java", "-cp", temp_dir, "Main"],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if run_result.returncode != 0:
            return f"__ERROR__: {run_result.stderr.strip()}"
        return run_result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"
    except Exception as e:
        return f"__ERROR__: {e}"