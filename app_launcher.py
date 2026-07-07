import os
import webbrowser

APP_COMMANDS = {
    "calculator": "calc",
    "calci": "calc",
    "calc": "calc",

    "notepad": "notepad",

    "paint": "mspaint",
    "ms paint": "mspaint",
    "mspaint": "mspaint",

    "cmd": "cmd",
    "command prompt": "cmd",

    "file explorer": "explorer",
    "explorer": "explorer",

    "camera": "start microsoft.windows.camera:"
}


def open_app(app_name):

    app_name = app_name.lower().strip()

    # Websites
    if app_name == "youtube":
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    if app_name == "google":
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    # Chrome
    if app_name == "chrome":
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        if os.path.exists(chrome_path):
            os.startfile(chrome_path)
            return "Opening Chrome"

        return "Chrome not found"

    # Known Windows Apps
    if app_name in APP_COMMANDS:

        command = APP_COMMANDS[app_name]

        os.system(command)

        return f"Opening {app_name}"

    return f"I don't know how to open {app_name} yet."