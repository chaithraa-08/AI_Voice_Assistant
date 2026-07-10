import os


def file_manager_execute(action, parameters):

    action = action.lower()

    try:

        # Create Folder
        if action == "create" and "folder_name" in parameters:

            folder = parameters["folder_name"]
            os.makedirs(folder, exist_ok=True)

            return f"Folder '{folder}' created successfully."

        # Create File
        elif action == "create" and "file_name" in parameters:

            file = parameters["file_name"]

            with open(file, "w") as f:
                pass

            return f"File '{file}' created successfully."

        # Read File
        elif action == "read":

            file = parameters.get("file_name")

            if not os.path.exists(file):
                return "File not found."

            with open(file, "r") as f:
                content = f.read()

            return content if content else "File is empty."

        # Write File
        elif action == "write":

            file = parameters.get("file_name")
            content = parameters.get("content", "")

            with open(file, "w") as f:
                f.write(content)

            return f"Written successfully to '{file}'."

        # Delete File
        elif action == "delete":

            file = parameters.get("file_name")

            if os.path.exists(file):
                os.remove(file)
                return f"Deleted '{file}'."

            return "File not found."

        else:
            return "Unsupported file operation."

    except Exception as e:
        return str(e)