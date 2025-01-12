
from menu import (
    display_main_menu,
    display_input_menu,
    display_config_menu,
    display_circle_config,
    display_output_format_menu,
    clear_terminal
)
from detection import detect_circles_in_video
from config import load_config, save_config

def main():
    circle_params, output_params = load_config()

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
                            save_config(circle_params, output_params)

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
                                save_config(circle_params, output_params)
                            else:
                                print("Invalid format. Please try again.")
                        elif out_choice == '2':
                            new_format = input("Enter new image format ('jpg' or 'png'): ").strip().lower()
                            if new_format in ['jpg', 'png']:
                                output_params['image_format'] = new_format
                                save_config(circle_params, output_params)
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
                input_source = None
                is_file = False
                is_camera = False
                is_image = False

        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
