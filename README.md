# Optical Reference Stabiliser for CubeSat

This repository contains a Python-based optical reference stabiliser designed for CubeSat missions. It provides real-time circle (target) detection from various input sources (camera, video, or images) and automatically saves configuration settings and output files. The code is split across multiple modules for clarity, with persistent settings stored in a JSON file.

---

## Features
- **Real-Time Circle Detection**  
  Employs Hough Transform for circle detection in real time.
- **Multiple Input Modes**  
  Supports camera (live feed), video files, and still images.
- **Customisable Output**  
  Saves processed data in timestamped video/image formats (configurable in the menu).
- **Persistent Settings**  
  Stores detection parameters and output preferences in a `config.json` file for future sessions.
- **Timestamped Filenames**  
  Automatically names output files based on the current date and time.
- **Menu-Driven Interface**  
  Clear command-line menus for selecting inputs and adjusting settings.

---

## Requirements
- Python 3.7+  
- [OpenCV](https://opencv.org/) (cv2)
- NumPy
- (Optional) Any additional libraries for environment management and packaging

Install dependencies (example with pip):
```bash
pip install opencv-python numpy
```

---

## Getting Started

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/agastyahukoo/optical-reference-stabiliser.git
   cd optical-reference-stabiliser
   ```

2. **Run the Application**  
   ```bash
   python main.py
   ```
   This will generate a `config.json` on first launch if it does not exist.

3. **Follow the Menus**  
   - **Select Input**: Choose camera, video file, or image file.  
   - **Configuration**: Adjust circle detection parameters and output formats.  
   - **Start Detection**: View detections in real time. Press **q** in the display window to quit.

4. **Check Outputs**  
   - Processed videos or images are saved in the `output` folder, each file named with a timestamp (e.g. `output_2025_01_12_15_30_59.mp4`).

---

## Project Structure

```
├── main.py            # Application entry point and main menu
├── menu.py            # Menu display and utilities
├── detection.py       # Core circle detection and output logic
├── config.py          # Loads/saves settings from/to config.json
├── config.json        # Auto-generated persistent configuration
└── output/            # Output folder for processed videos/images
```

---

## Troubleshooting
- **Local Files Not Detected**: Ensure that you run `main.py` in the same directory as your files, or provide the absolute path.  
- **Dependencies**: Double-check that OpenCV and NumPy are correctly installed and compatible with your Python version.  
- **Permissions**: If writing to `output` fails, verify that you have sufficient file permissions.  

---

## Contributing
Contributions, suggestions, and bug reports are welcomed. Please open an issue or submit a pull request with relevant details. 

---

## Disclaimer
This software is provided as-is for demonstration and development purposes in a CubeSat context. It is **not** guaranteed to meet flight software requirements without further testing and validation.  

---

## Licence
This project is available under the [MIT Licence](https://opensource.org/licenses/MIT).  
