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
    def __init__(self, threshold, model1, model2, snapshot_dir, max_movements=3, buffer_size=50, camera_index=0):
        self.camera_index = camera_index  # Store the camera index
        self.threshold = threshold
        self.motion_buffer = []  # Buffer for detected motions
        self.model1 = model1
        self.model2 = model2
        self.notification_id = None  # Ensure notification_id is always defined
        self.max_movements = max_movements
        self.movement_buffer = collections.deque(maxlen=buffer_size)

        # Detection state variables
        self.looking_around_count = 0
        self.reaching_detected = False
        self.concealing_detected = False
        self.theft_warning_active = False
        self.theft_warning_start_time = None
        self.theft_detected = False  # New flag to confirm theft
        self.current_action = "None"
        self.current_prob = 0.0
        
        # Flags to track if snapshots have already been saved for each action
        self.looking_around_saved = False
        self.reaching_saved = False
        self.concealing_saved = False

        # Mediapipe setup for drawing
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Database connection setup
        self.db_connection = self.connect_to_database()

        # Set the directory for saving snapshots
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)  # Ensure the directory exists

    def connect_to_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='theftpredictiondb'
        )

    def save_snapshot_to_db(self, file_path, user_id):
        try:
            file_name = os.path.basename(file_path)
            cursor = self.db_connection.cursor()

            # Insert into notifications, setting motion_id to NULL
            query = "INSERT INTO notifications (user_id, screenshots) VALUES (%s, %s)"
            cursor.execute(query, (user_id, file_name))
            self.db_connection.commit()
            
            # Get the inserted notification's ID
            notification_id = cursor.lastrowid
            return notification_id
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        finally:
            cursor.close()

    def save_motion_snapshot_to_db(self, name, file_path, threshold, notification_id):
        try:
            # Multiply the threshold by 100 before saving
            threshold *= 100
            file_name = os.path.basename(file_path)
            cursor = self.db_connection.cursor()

            # Insert motion and link it to the notification_id
            query = "INSERT INTO motions (name, notification_id, video_path, threshold) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, notification_id, file_name, float(threshold)))
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
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

    # def update_movement_buffer(self, action, frame):
    #     if action in ["left", "right"]:
    #         self.movement_buffer.append(action)
    #         changes = sum(1 for i in range(1, len(self.movement_buffer)) if self.movement_buffer[i] != self.movement_buffer[i - 1])
    #         if changes >= self.max_movements:
    #             self.looking_around_count = 1  # "Looking around" detected


    def update_movement_buffer(self, action, prob, frame):
        if action in ["left", "right"]:
            self.movement_buffer.append((action, prob))  # Store action and probability
            changes = sum(1 for i in range(1, len(self.movement_buffer)) if self.movement_buffer[i][0] != self.movement_buffer[i - 1][0])
            
            if changes >= self.max_movements:
                self.looking_around_count = 1  # "Looking around" detected
                avg_prob = np.mean([item[1] for item in self.movement_buffer])  # Calculate average probability

                if not self.looking_around_saved:
                    self.motion_buffer.append(("looking_around", frame, avg_prob))  # Buffer for later saving
                    self.looking_around_saved = True  # Mark as detected and buffered


    def save_potential_theft(self, frame):
        # Save potential theft snapshot
        file_path = self.save_snapshot(frame, "potential_theft")
        self.notification_id = self.save_snapshot_to_db(file_path, user_id=3)  # Create notification

        if self.notification_id:
            self.save_buffered_motions()  # Save all motions after notification_id is available


    def save_buffered_motions(self):
        for motion_type, frame, prob in self.motion_buffer:
            file_path = self.save_snapshot(frame, motion_type)
            self.save_motion_snapshot_to_db(motion_type, file_path, prob, self.notification_id)
        self.motion_buffer.clear()  # Clear the buffer after saving


    def predict_pose(self, results, frame):
        if results.pose_landmarks:
            pose_row = list(np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in results.pose_landmarks.landmark]).flatten())
            X = pd.DataFrame([pose_row])

            if self.looking_around_count == 0:
                self.current_action = self.model1.predict(X)[0]
                self.current_prob = self.model1.predict_proba(X)[0].max()
                if self.current_prob >= self.threshold:
                    self.update_movement_buffer(self.current_action, self.current_prob, frame)
            else:
                self.current_action = self.model2.predict(X)[0]
                self.current_prob = self.model2.predict_proba(X)[0].max()
                if self.current_prob >= 0.77:
                    if self.current_action == "reach" and not self.reaching_detected:
                        self.reaching_detected = True
                        self.motion_buffer.append(("reaching", frame, self.current_prob))

                    elif self.current_action == "conceal" and not self.concealing_detected:
                        if self.reaching_detected:
                            self.concealing_detected = True
                            self.motion_buffer.append(("concealing", frame, self.current_prob))

            # Check for potential theft
            if self.looking_around_count == 1 and self.reaching_detected and self.concealing_detected:
                if not self.theft_detected:
                    self.theft_detected = True
                    self.save_potential_theft(frame)


    def display_results(self, image, results):
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)

            # Status text display
            status_text = [
                f"Looking Around Detected: {'Yes' if self.looking_around_count else 'No'}",
                f"Reaching Detected: {'Yes' if self.reaching_detected else 'No'}",
                f"Concealing Detected: {'Yes' if self.concealing_detected else 'No'}"
            ]

            for i, text in enumerate(status_text):
                cv2.putText(image, text, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Trigger potential theft logic when all actions are detected
            if self.looking_around_count == 1 and self.reaching_detected and self.concealing_detected:
                if not self.theft_warning_active:
                    self.theft_warning_active = True
                    self.theft_warning_start_time = time.time()

                    # Save potential theft notification
                    if not self.notification_id:
                        file_path = self.save_snapshot(image, "potential_theft")
                        self.notification_id = self.save_snapshot_to_db(file_path, user_id=3)


                # Reset flags after 2 seconds
                if time.time() - self.theft_warning_start_time >= 2:
                    self.reset_detection_flags()



    def reset_detection_flags(self):
        self.theft_warning_active = False
        self.notification_id = None  # Clear for next cycle
        self.looking_around_count = 0
        self.reaching_detected = False
        self.concealing_detected = False
        self.looking_around_saved = False
        self.reaching_saved = False
        self.concealing_saved = False
        self.motion_save_lock = False
        self.theft_saved = False
        self.theft_detected = False
        self.motion_buffer.clear()  # Clear buffered motions
        self.movement_buffer.clear()

   

    def generate_frames(self):
        cap = cv2.VideoCapture(self.camera_index)  # Use dynamic camera index
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

@app.route('/video_feed')
def video_feed():
    return Response(detector.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Modify the start_server method to pass the snapshot directory
def start_server():
    global detector  # Declare the detector variable as global at the start of the method
    
    if model1 is None or model2 is None:
        messagebox.showwarning("Warning", "Please load both models before starting the server.")
        return
    
    snapshot_dir = detector.snapshot_dir  # Use the dynamic directory, after it's selected
    if not snapshot_dir:  # Check if a directory is selected
        messagebox.showwarning("Warning", "Please select a snapshot folder first.")
        return
    
    camera_index = int(camera_index_entry.get())
    detector = BodyLanguageDetector(0.7, model1, model2, snapshot_dir)  # Initialize detector
    threading.Thread(target=start_flask_server, daemon=True).start()
    
    # Minimize the GUI window
    root.iconify()
    messagebox.showinfo("Info", "Server started on http://localhost:5000/video_feed")

# GUI method to select snapshot directory
def select_snapshot_directory():
    global detector  # Declare the detector variable as global
    
    snapshot_dir = filedialog.askdirectory(title="Select Snapshot Folder")
    if snapshot_dir:
        if model1 is None or model2 is None:
            messagebox.showwarning("Warning", "Please load both models before selecting a snapshot folder.")
            return
        
        # Initialize the detector object if it's not already initialized
        if detector is None:
            camera_index = int(camera_index_entry.get())
            detector = BodyLanguageDetector(0.7, model1, model2, snapshot_dir)  # Initialize detector

        detector.snapshot_dir = snapshot_dir  # Set the new snapshot directory
        messagebox.showinfo("Info", f"Snapshot directory set to: {snapshot_dir}")
    else:
        messagebox.showwarning("Warning", "No directory selected!")


    

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
root.geometry("400x400")

# Camera input field
camera_index_label = ctk.CTkLabel(root, text="Enter Camera Index:")
camera_index_label.pack(pady=10)

camera_index_entry = ctk.CTkEntry(root)
camera_index_entry.pack(pady=10)
camera_index_entry.insert(0, "0")  # Default to 0 if no input

# Buttons
head_motion_btn = ctk.CTkButton(root, text="Load Head Motion Model", command=load_head_motion_model)
head_motion_btn.pack(pady=20)

gesture_motion_btn = ctk.CTkButton(root, text="Load Gesture Model", command=load_gesture_model)
gesture_motion_btn.pack(pady=20)

# Add a button to select the directory for snapshots
select_dir_btn = ctk.CTkButton(root, text="Select Snapshot Folder", command=select_snapshot_directory)
select_dir_btn.pack(pady=10)

start_btn = ctk.CTkButton(root, text="Start", command=start_server)
start_btn.pack(pady=20)

root.mainloop()
