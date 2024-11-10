import customtkinter as ctk
import collections
import mediapipe as mp
from tkinter import filedialog, messagebox
import threading
from flask import Flask, Response
import pickle
import numpy as np
import pandas as pd
import cv2
import os
import mysql.connector
import time

# Flask app
app = Flask(__name__)

# Global variables for models
model1 = None
model2 = None
detector = None

class BodyLanguageDetector:
    def __init__(self, threshold, model1, model2, max_movements=3, buffer_size=50):
        self.threshold = threshold
        self.model1 = model1
        self.model2 = model2
        self.max_movements = max_movements
        self.movement_buffer = collections.deque(maxlen=buffer_size)

        # Detection state variables
        self.looking_around_count = 0
        self.reaching_detected = False
        self.concealing_detected = False
        self.theft_warning_active = False
        self.theft_warning_start_time = None
        self.current_action = "None"
        self.current_prob = 0.0

        # Mediapipe setup for drawing
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Database connection setup
        self.db_connection = self.connect_to_database()

        # Set the directory for saving snapshots
        self.snapshot_dir = r'C:\Users\Kent\Desktop\Coding Portfolio\FULL STACK DEV\Thesis_v3\view\public\Snapshots'
        os.makedirs(self.snapshot_dir, exist_ok=True)  # Ensure the directory exists

    def connect_to_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='theftpredictiondb'
        )

    def save_snapshot_to_db(self, file_path, name, user_id):
        # Extract only the file name from the full path
        file_name = os.path.basename(file_path)
        cursor = self.db_connection.cursor()
        query = "INSERT INTO notifications (screenshots, motion_id, user_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (file_name, name, user_id))
        self.db_connection.commit()
        cursor.close()

    def save_snapshot(self, image, action_type):
        file_name = f"{int(time.time())}_{action_type}.jpg"  # Create a unique file name
        file_path = os.path.join(self.snapshot_dir, file_name)
        cv2.imwrite(file_path, image)  # Save the image to the specified directory
        return file_path

    def process_frame(self, frame):
        frame_resized = cv2.resize(frame, (1280, int(1280 * frame.shape[0] / frame.shape[1])))
        image_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        results = self.mp_holistic.process(image_rgb)
        return cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR), results

    def update_movement_buffer(self, action, frame):
        if action in ["left", "right"]:
            self.movement_buffer.append(action)
            changes = sum(1 for i in range(1, len(self.movement_buffer)) if self.movement_buffer[i] != self.movement_buffer[i - 1])
            if changes >= self.max_movements:
                self.looking_around_count = 1  # "Looking around" detected
                # file_path = self.save_snapshot(frame, "looking_around")  # Take snapshot and save path
                # self.save_snapshot_to_db(file_path, 1, 3)  # Save path to DB

    def predict_pose(self, results, frame):
        if results.pose_landmarks:
            pose_row = list(np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in results.pose_landmarks.landmark]).flatten())
            X = pd.DataFrame([pose_row])

            # Determine which model to use based on "looking around" state
            if self.looking_around_count == 0:  # Use Head pose model if not looking around
                self.current_action = self.model1.predict(X)[0]
                self.current_prob = self.model1.predict_proba(X)[0].max()
                if self.current_prob >= self.threshold:
                    self.update_movement_buffer(self.current_action, frame)  # Pass the frame for snapshot
                else:
                    self.current_action = "None"
                    self.current_prob = 0.0
            else:  # Use Gesture model if looking around
                self.current_action = self.model2.predict(X)[0]
                self.current_prob = self.model2.predict_proba(X)[0].max()
                if self.current_prob >= 0.77:
                    if self.current_action == "reach":
                        self.reaching_detected = True
                        # file_path = self.save_snapshot(frame, "reaching")  # Take snapshot and save path
                        # self.save_snapshot_to_db(file_path, 2, 3)  # Save path to DB
                    elif self.current_action == "conceal":
                        if self.reaching_detected:
                            self.concealing_detected = True
                        # file_path = self.save_snapshot(frame, "conceal")  # Take snapshot and save path
                        # self.save_snapshot_to_db(file_path, 3, 3)  # Save path to DB
                else:
                    self.current_action = "None"
                    self.current_prob = 0.0

    def display_results(self, image, results):
        # Draw body landmarks and connections
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)

            left_ear = results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_EAR]
            left_ear_pos = (int(left_ear.x * image.shape[1]), int(left_ear.y * image.shape[0]))

            action_text = f"{self.current_action} ({self.current_prob:.2f})"
            cv2.putText(image, action_text, (left_ear_pos[0] + 10, left_ear_pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Status text display at the left side of the frame
        status_text = [
            f"Looking Around Detected: {'Yes' if self.looking_around_count else 'No'}",
            f"Reaching Detected: {'Yes' if self.reaching_detected else 'No'}",
            f"Concealing Detected: {'Yes' if self.concealing_detected else 'No'}"
        ]

        for i, text in enumerate(status_text):
            cv2.putText(image, text, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Check and display potential theft warning
        if self.looking_around_count == 1 and self.reaching_detected and self.concealing_detected:
            if not self.theft_warning_active:
                self.theft_warning_active = True
                self.theft_warning_start_time = time.time()
                file_path = self.save_snapshot(image, "potential_theft")  # Take snapshot for potential theft
                self.save_snapshot_to_db(file_path, 1, 3)  # Save path to DB
            # if self.theft_warning_active:
            #     cv2.putText(image, 'POTENTIAL THEFT DETECTED', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

            if time.time() - self.theft_warning_start_time >= 2:  # Show warning for 2 seconds
                self.theft_warning_active = False
                self.looking_around_count = 0
                self.reaching_detected = False
                self.concealing_detected = False
                self.movement_buffer.clear()

    def generate_frames(self):
        cap = cv2.VideoCapture(0)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                image, results = self.process_frame(frame)
                self.predict_pose(results, frame)  # Update actions based on model predictions
                self.display_results(image, results)  # Show action indicators and theft warning if needed

                _, buffer = cv2.imencode('.jpg', image)  # Use 'image' instead of 'frame'
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        finally:
            cap.release()
            # cv2.destroyAllWindows()
            # self.db_connection.close()

@app.route('/video_feed')
def video_feed():
    return Response(detector.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False)

def start_server():
    if model1 is None or model2 is None:
        messagebox.showwarning("Warning", "Please load both models before starting the server.")
        return
    global detector
    detector = BodyLanguageDetector(0.7, model1, model2)
    threading.Thread(target=start_flask_server, daemon=True).start()
        # Minimize the GUI window
    root.iconify()
    messagebox.showinfo("Info", "Server started on http://localhost:5000/video_feed")

def load_head_motion_model():
    global model1
    file_path = filedialog.askopenfilename(title="Select Head Motion Model", filetypes=[("Pickle files", "*.pkl")])
    if file_path:
        with open(file_path, 'rb') as f:
            model1 = pickle.load(f)
        messagebox.showinfo("Info", "Head motion model loaded successfully.")

def load_gesture_model():
    global model2
    file_path = filedialog.askopenfilename(title="Select Gesture Model", filetypes=[("Pickle files", "*.pkl")])
    if file_path:
        with open(file_path, 'rb') as f:
            model2 = pickle.load(f)
        messagebox.showinfo("Info", "Gesture model loaded successfully.")

# Initialize customtkinter
ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

# GUI layout
root = ctk.CTk()
root.title("Body Language Detection")
root.geometry("400x300")

# Buttons
head_motion_btn = ctk.CTkButton(root, text="Load Head Motion Model", command=load_head_motion_model)
head_motion_btn.pack(pady=20)

gesture_motion_btn = ctk.CTkButton(root, text="Load Gesture Model", command=load_gesture_model)
gesture_motion_btn.pack(pady=20)

start_btn = ctk.CTkButton(root, text="Start", command=start_server)
start_btn.pack(pady=20)

root.mainloop()

