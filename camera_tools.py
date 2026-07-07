import cv2
from datetime import datetime

def take_photo():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if ret:

        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        cv2.imwrite(filename, frame)

        cap.release()

        return f"Photo saved as {filename}"

    cap.release()

    return "Could not capture photo"