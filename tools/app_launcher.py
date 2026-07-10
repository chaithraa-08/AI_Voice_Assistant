import subprocess
import os


APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
    "vscode": "code"
}


def launch_app(app_name):

    app = app_name.lower()

    if app not in APP_PATHS:
        return f"Application '{app_name}' is not supported."

    try:

        path = APP_PATHS[app]

        if os.path.exists(path):
            subprocess.Popen(path)
        else:
            subprocess.Popen(path, shell=True)

        return f"{app_name} opened successfully."

    except Exception as e:
        return str(e)