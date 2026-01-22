import os
import platform
import subprocess
import sys


def run_django_commands():
    # Determine the python command
    python_cmd = "python"
    if platform.system() != "Windows":
        python_cmd = "python3"  # Linux/Mac often use python3

    commands = [
        f"{python_cmd} manage.py makemigrations",
        f"{python_cmd} manage.py migrate",
        f"{python_cmd} manage.py runserver",
    ]

    for cmd in commands:
        print(f"\nRunning: {cmd}\n")
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()  # Wait for command to finish


if __name__ == "__main__":
    run_django_commands()
