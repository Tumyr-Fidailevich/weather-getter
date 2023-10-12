from subprocess import CalledProcessError, check_call

REQUIREMENTS_FILE = 'requirements.txt'

try:
    check_call(['pip', 'install', '-r', REQUIREMENTS_FILE])
    print("Environment installed successfully")
except CalledProcessError as e:
    print("Error during installing environment :", e)
