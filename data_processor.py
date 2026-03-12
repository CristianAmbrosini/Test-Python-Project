import hashlib
import subprocess
import os
import yaml


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def run_command(user_input):
    result = subprocess.run(f"echo {user_input}", shell=True, capture_output=True, text=True)
    return result.stdout


def read_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def compute_average(values):
    total = 0
    for v in values:
        total += v
    return total / len(values)


def save_report(filename, content):
    path = os.path.join("/tmp", filename)
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, 0o777)
    return path
