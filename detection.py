import cv2
import numpy as np
import time
import os
from menu import clear_terminal
from config import save_config
from datetime import datetime

def process_and_display_frame(frame, circle_params):
    """
    Process a single frame (or image) for circle detection and return the annotated frame.
    """
    start_time = time.time()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=circle_params['dp'],
        minDist=circle_params['minDist'],
        param1=circle_params['param1'],
        param2=circle_params['param2'],
        minRadius=circle_params['minRadius'],
        maxRadius=circle_params['maxRadius']
    )

    end_time = time.time()
    clear_terminal()
    print(f"Frame processing time: {end_time - start_time:.4f} seconds")

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(frame, center, 5, (0, 255, 0), -1)  # Center
            cv2.circle(frame, center, radius, (255, 0, 0), 2)
    else:
        print("No circles detected in this frame.")
    return frame

def handle_image_output(frame, output_params):
    """
    Saves the processed image if the user chooses.
    """
    save_output = input("Do you want to save the processed image? (yes/no): ").strip().lower()
    if save_output in ['yes', 'y']:
        output_folder = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        img_ext = output_params['image_format']
        output_path = os.path.join(output_folder, f"output_{timestamp}.{img_ext}")

        cv2.imwrite(output_path, frame)
        print(f"Processed image saved to: {output_path}")

    cv2.imshow("Detected Circles", frame)
    print("Press any key in the image window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_circles_in_video(
    source,
    circle_params,
    output_params,
    is_file=False,
    is_camera=False,
    is_image=False
):
    """
    source        : path to file or camera index
    circle_params : dict with circle detection parameters
    output_params : dict with output settings (video/image formats)
    is_file       : True if input is a video file
    is_camera     : True if input is camera stream
    is_image      : True if input is an image
    """

    if is_image:
        if not os.path.isabs(source):
            source = os.path.join(os.getcwd(), source)
        frame = cv2.imread(source)
        if frame is None:
            print(f"Error: Unable to open image '{source}'.")
            return
        processed_frame = process_and_display_frame(frame, circle_params)
        handle_image_output(processed_frame, output_params)
        return
    else:
        if is_file:
            if not os.path.isabs(source):
                source = os.path.join(os.getcwd(), source)
            cap = cv2.VideoCapture(source)
        elif is_camera:
            cap = cv2.VideoCapture(int(source))
        else:
            print("Invalid input source specified.")
            return

    if not cap.isOpened():
        print(f"Error: Unable to open video/camera source '{source}'.")
        return

    record_output = input("Do you want to save the output? (yes/no): ").strip().lower()
    out = None
    output_path = None

    if record_output in ['yes', 'y']:
        output_folder = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        video_ext = output_params['video_format']
        output_path = os.path.join(output_folder, f"output_{timestamp}.{video_ext}")

        fourcc = cv2.VideoWriter_fourcc(*('XVID' if video_ext == 'avi' else 'mp4v'))
        print(f"Output will be saved to: {output_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (960, 540))

        processed_frame = process_and_display_frame(frame, circle_params)

        if record_output in ['yes', 'y']:
            if out is None:
                frame_height, frame_width = processed_frame.shape[:2]
                out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height))
            out.write(processed_frame)

        cv2.imshow('Detected Circles', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

    save_config(circle_params, output_params)
