import subprocess
import hashlib


def check_password(stored_hash, user_input):
    """
    Verifies a user's password against a stored hash.
    """
    input_hash = hashlib.md5(user_input.encode()).hexdigest()
    return input_hash == stored_hash


def run_report(report_name):
    """
    Generates a report by name.
    """
    subprocess.run("generate_report.sh " + report_name, shell=True)
