import cv2
import os
from datetime import datetime


def camera_execute(action, parameters):

    action = action.lower()

    try:

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return "Unable to access camera."

        ret, frame = camera.read()

        if not ret:
            camera.release()
            return "Failed to capture image."

        if action == "capture":

            os.makedirs("captures", exist_ok=True)

            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            filepath = os.path.join("captures", filename)

            cv2.imwrite(filepath, frame)

            camera.release()

            return f"Image saved as {filepath}"

        elif action == "open":

            while True:

                cv2.imshow("Camera", frame)

                ret, frame = camera.read()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            camera.release()
            cv2.destroyAllWindows()

            return "Camera closed."

        else:

            camera.release()
            return "Unsupported camera action."

    except Exception as e:
        return str(e)