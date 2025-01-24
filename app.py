from flask import Flask, render_template, request, Response, jsonify
import cv2
import os
import json
import numpy as np

app = Flask(__name__)

config_file_path = "config.json"
if not os.path.exists(config_file_path):
    raise FileNotFoundError("config.json not found!")

with open(config_file_path, "r") as f:
    config = json.load(f)

circle_params = config.get("circle_params", {})
output_params = config.get("output_params", {})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_frame(frame):
    frame = cv2.resize(frame, (960, 540))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=circle_params["dp"],
        minDist=circle_params["minDist"],
        param1=circle_params["param1"],
        param2=circle_params["param2"],
        minRadius=circle_params["minRadius"],
        maxRadius=circle_params["maxRadius"]
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            cv2.circle(frame, center, radius, (255, 0, 0), 2)
    return frame

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    file_name = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, file_name)
    file.save(save_path)
    return jsonify({"file_path": file_name})

@app.route("/video_feed/<filename>")
def video_feed(filename):
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    def generate_frames():
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return
        while True:
            success, frame = cap.read()
            if not success:
                break
            processed_frame = process_frame(frame)
            ret, buffer = cv2.imencode(".jpg", processed_frame)
            if not ret:
                break
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   buffer.tobytes() +
                   b"\r\n")
        cap.release()
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/get_settings", methods=["GET"])
def get_settings():
    return jsonify({
        "circle_params": circle_params,
        "output_params": output_params
    })

@app.route("/update_settings", methods=["POST"])
def update_settings():
    new_config = request.json
    circle_params.update(new_config["circle_params"])
    output_params.update(new_config["output_params"])
    with open(config_file_path, "w") as f:
        json.dump({
            "circle_params": circle_params,
            "output_params": output_params
        }, f, indent=4)
    return jsonify({"message": "Settings updated"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
