import cv2
import numpy as np
import time
import os


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu():
    clear_terminal()
    print("===============================================")
    print("         Circle Detection - Main Menu          ")
    print("===============================================")
    print("[1] Select Input (Camera, Video, Image)")
    print("[2] Configuration / Settings")
    print("[3] Start Detection")
    print("[4] Quit")
    print("===============================================")

def display_input_menu():
    clear_terminal()
    print("===============================================")
    print("       Circle Detection - Input Menu           ")
    print("===============================================")
    print("[1] Camera")
    print("[2] Video File")
    print("[3] Image File")
    print("[4] Back to Main Menu")
    print("===============================================")

def display_config_menu():
    clear_terminal()
    print("===============================================")
    print("    Circle Detection - Configuration Menu      ")
    print("===============================================")
    print("[1] Set Circle Detection Parameters (Hough)")
    print("[2] Set Output Format")
    print("[3] Back to Main Menu")
    print("===============================================")

def display_circle_config(params):
    clear_terminal()
    print("===============================================")
    print("   Current Circle Detection Parameters (Hough) ")
    print("===============================================")
    print(f"1) dp:            {params['dp']}")
    print(f"2) minDist:       {params['minDist']}")
    print(f"3) param1:        {params['param1']}")
    print(f"4) param2:        {params['param2']}")
    print(f"5) minRadius:     {params['minRadius']}")
    print(f"6) maxRadius:     {params['maxRadius']}")
    print("===============================================")
    print("[7] Back to Config Menu")
    print("===============================================")

def display_output_format_menu(output_params):
    clear_terminal()
    print("===============================================")
    print("       Circle Detection - Output Format        ")
    print("===============================================")
    print(f"1) Output video format:  {output_params['video_format']}")
    print(f"2) Output image format:  {output_params['image_format']}")
    print("===============================================")
    print("[3] Back to Config Menu")
    print("===============================================")

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

    if is_camera:
        cap = cv2.VideoCapture(int(source)) 
    elif is_file:
        cap = cv2.VideoCapture(source)
    elif is_image:
        frame = cv2.imread(source)
        if frame is None:
            print(f"Error: Unable to open image '{source}'.")
            return
        process_and_display_frame(frame, circle_params)
        handle_image_output(frame, output_params)
        return
    else:
        print("Invalid input source specified.")
        return

    if not cap.isOpened():
        print("Error: Unable to open video/camera.")
        return

    record_output = input("Do you want to save the output? (yes/no): ").strip().lower()
    out = None
    if record_output in ['yes', 'y']:
        output_folder = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        video_ext = output_params['video_format']
        output_path = os.path.join(output_folder, f'output.{video_ext}')

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
            cv2.circle(frame, center, 5, (0, 255, 0), -1)  
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
        img_ext = output_params['image_format']
        output_path = os.path.join(output_folder, f'output.{img_ext}')
        cv2.imwrite(output_path, frame)
        print(f"Processed image saved to: {output_path}")

    cv2.imshow("Detected Circles", frame)
    print("Press any key in the image window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    circle_params = {
        'dp': 1.2,
        'minDist': 1000,
        'param1': 100,
        'param2': 30,
        'minRadius': 150,
        'maxRadius': 300
    }

    output_params = {
        'video_format': 'mp4',  
        'image_format': 'jpg'   
    }

    input_source = None
    is_file = False
    is_camera = False
    is_image = False

    while True:
        display_main_menu()
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            while True:
                display_input_menu()
                inp_choice = input("Select input source: ").strip()
                if inp_choice == '1':
                    input_source = 0  
                    is_camera = True
                    is_file = False
                    is_image = False
                    break
                elif inp_choice == '2':
                    video_path = input("Enter the path to the video file: ").strip()
                    input_source = video_path
                    is_file = True
                    is_camera = False
                    is_image = False
                    break
                elif inp_choice == '3':
                    image_path = input("Enter the path to the image file: ").strip()
                    input_source = image_path
                    is_image = True
                    is_camera = False
                    is_file = False
                    break
                elif inp_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == '2':
            while True:
                display_config_menu()
                config_choice = input("Select an option: ").strip()
                if config_choice == '1':
                    while True:
                        display_circle_config(circle_params)
                        param_choice = input("Choose parameter to edit (1-6, or 7 to go back): ").strip()
                        if param_choice in ['1','2','3','4','5','6']:
                            new_val = input("Enter new value (integer): ").strip()
                            try:
                                new_val = int(new_val)
                            except ValueError:
                                print("Invalid integer value. Try again.")
                                continue
                            if param_choice == '1':
                                circle_params['dp'] = new_val
                            elif param_choice == '2':
                                circle_params['minDist'] = new_val
                            elif param_choice == '3':
                                circle_params['param1'] = new_val
                            elif param_choice == '4':
                                circle_params['param2'] = new_val
                            elif param_choice == '5':
                                circle_params['minRadius'] = new_val
                            elif param_choice == '6':
                                circle_params['maxRadius'] = new_val
                        elif param_choice == '7':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif config_choice == '2':
                    while True:
                        display_output_format_menu(output_params)
                        out_choice = input("Select an option: ").strip()
                        if out_choice == '1':
                            new_format = input("Enter new video format ('mp4' or 'avi'): ").strip().lower()
                            if new_format in ['mp4', 'avi']:
                                output_params['video_format'] = new_format
                            else:
                                print("Invalid format. Please try again.")
                        elif out_choice == '2':
                            new_format = input("Enter new image format ('jpg' or 'png'): ").strip().lower()
                            if new_format in ['jpg', 'png']:
                                output_params['image_format'] = new_format
                            else:
                                print("Invalid format. Please try again.")
                        elif out_choice == '3':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif config_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == '3':
            # Start Detection
            if input_source is None:
                print("No input selected. Please select an input source first.")
            else:
                detect_circles_in_video(
                    source=input_source,
                    circle_params=circle_params,
                    output_params=output_params,
                    is_file=is_file,
                    is_camera=is_camera,
                    is_image=is_image
                )
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
