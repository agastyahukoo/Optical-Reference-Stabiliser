# menu.py

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
