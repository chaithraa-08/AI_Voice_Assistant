import os
import ctypes


def system_control_execute(action, parameters):

    action = action.lower()

    try:

        if action == "lock":
            ctypes.windll.user32.LockWorkStation()
            return "Computer locked."

        elif action == "restart":
            os.system("shutdown /r /t 5")
            return "Restarting computer in 5 seconds."

        elif action == "shutdown":
            os.system("shutdown /s /t 5")
            return "Shutting down computer in 5 seconds."

        elif action == "cancel":
            os.system("shutdown /a")
            return "Shutdown/Restart cancelled."

        else:
            return "Unsupported system control action."

    except Exception as e:
        return str(e)