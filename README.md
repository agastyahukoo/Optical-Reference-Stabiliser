# Optical Stabilisation System

A web-based application for **circle detection** and **reference image stabilization**, featuring:
- **Video Upload** and live-processed playback in the browser
- **Circle Detection** with configurable Hough Transform parameters
- **Settings Panel** to adjust and persist detection or output configurations
- **Dark-Themed UI** for a modern and minimal look

## Features

- **Upload & Detect**: Users can upload video files, which are processed frame-by-frame to detect circles.
- **Live Preview**: The processed video is streamed back to the browser in real time using Flask’s `Response` streaming.
- **Configurable Parameters**: The built-in **Settings** panel lets you modify Hough Circle detection parameters (`dp`, `minDist`, `param1`, `param2`, `minRadius`, `maxRadius`) and adjust output formats (`video_format`, `image_format`) — updates are saved to `config.json`.
- **Toggleable Settings Panel**: Quickly pause (hide) the video to tweak parameters, then resume processing with new settings.

## Requirements

- **Python 3.7+**  
- **Flask 2.0+**  
- **OpenCV 4.x**  
- **NumPy**  

*(See `requirements.txt` or install via `pip install flask opencv-python numpy`.)*

## Getting Started

1. **Clone** this repository:
   ```bash
   git clone https://github.com/agastyahukoo/Optical-Reference-Stabiliser.git
   cd Optical-Reference-Stabiliser
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Or manually install the required Python packages.)*

3. **Configure `config.json`**:
   ```json
   {
       "circle_params": {
           "dp": 1.2,
           "minDist": 1000,
           "param1": 100,
           "param2": 30,
           "minRadius": 150,
           "maxRadius": 300
       },
       "output_params": {
           "video_format": "avi",
           "image_format": "jpg"
       }
   }
   ```
   Adjust initial detection or output parameters here.

4. **Run the Flask server**:
   ```bash
   python app.py
   ```
   By default, the app runs at `http://127.0.0.1:5000`.

5. **Open Your Browser** at `http://127.0.0.1:5000`:
   - Click **Choose File**, select a video, and **Upload**.
   - The processed video stream will appear.  
   - **Settings** lets you pause the preview and adjust circle detection or output settings. Click **Save & Close** to apply changes.

## How It Works

1. Uploaded videos are saved in the `uploads/` folder.  
2. Frames are processed with Hough Circle detection (CLAHE > Gaussian Blur > HoughCircles).  
3. The **Settings** panel updates `config.json` in real time, so new frames use the updated parameters.  

## Contributing

Feel free to **open issues** or **create pull requests** for improvements, bug fixes, or new features. Any help is appreciated!

## License

This project is made available under the [MIT License](LICENSE).  
