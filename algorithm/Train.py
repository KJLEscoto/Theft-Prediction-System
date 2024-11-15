import customtkinter as ctk
import tkinter.messagebox as msgbox
from customtkinter import E, N, NE, NO, NORMAL, NS, ON, S, SE, TOP, W, X, Y
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import tkinter
import cv2
import mediapipe as mp
import numpy as np
import csv
import threading
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import mysql.connector
import time
ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

class MotionFeedApp:

    def __init__(self, root):
        self.root = root
        self.file_name_var = tk.StringVar()
        self.camera_index_var = tk.StringVar(value="0")  # Default to camera 0
        self.training_handler = TrainingHandler()
        self.setup_ui()

    def save_to_database(self, class_name):
        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='theftpredictiondb'
            )

            cursor = connection.cursor()

            # Create the insert query
            query = """
            INSERT INTO motions (name, description, video_path, threshold)
            VALUES (%s, %s, %s, %s)
            """

            # Prepare the data to insert
            name = class_name
            description = f"this is the {class_name}"
            video_path = f"{class_name}mp4"
            threshold = 95.23

            # Execute the query
            cursor.execute(query, (name, description, video_path, threshold))

            # Commit the transaction
            connection.commit()

            print(f"Data for {class_name} saved successfully!")

        except mysql.connector.Error as e:
            print(f"Error saving to database: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def setup_ui(self):
        self.root.title('Train GUI')
        self.root.geometry('600x250')  # Increased window size for better UI display
        ctk.CTkLabel(self.root, text='Motion Feed', font=('Helvetica', 20)).pack(pady=10)
        ctk.CTkLabel(self.root, text='Choose an option you want to add a motion:').pack(pady=10)
        ctk.CTkButton(self.root, text='Via Live', command=self.show_webcam_gui).pack(pady=10)
        ctk.CTkButton(self.root, text='Via Video Feed', command=self.show_folder_gui).pack(pady=10)
        ctk.CTkButton(self.root, text='Via Image Feed', command=self.show_image_feed_gui).pack(pady=10)

    def upload_file(self):
        file = filedialog.askopenfile()
        if file:
            self.file_name_var.set(file.name)

    def enable_start_training_button(self):
        self.start_training_button.configure(state='normal')


    def get_available_cameras(self):
        """ Dynamically checks for available cameras. """
        index = 0
        available_cameras = {}
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                cap.release()
                break
            available_cameras[f"Camera {index}"] = str(index)
            cap.release()
            index += 1
        return available_cameras



    def show_webcam_gui(self):
        self.root.withdraw()
        webcam_window = ctk.CTkToplevel(self.root)
        webcam_window.title('Webcam Processing')
        webcam_window.geometry('600x250')

        # Class Name
        ctk.CTkLabel(webcam_window, text='Class Name:').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        file_name_entry = ctk.CTkEntry(webcam_window, textvariable=self.file_name_var)
        file_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Camera Index Dropdown
        ctk.CTkLabel(webcam_window, text='Camera Index:').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        available_cameras = self.get_available_cameras()  # Use self to call the method
        if not available_cameras:
            available_cameras = {"No Camera Found": "-1"}
            
        camera_index_dropdown = ctk.CTkOptionMenu(
            webcam_window,
            variable=self.camera_index_var,
            values=list(available_cameras.values())
        )
        camera_index_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Start Webcam Button
        ctk.CTkButton(webcam_window, text='Start Webcam', command=self.start_webcam).grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # Start Training Button
        csv_file = 'gesture.csv'
        self.start_training_button = ctk.CTkButton(
            webcam_window,
            text='Start Training',
            state='disabled',
            command=lambda: self.training_handler.start_training(csv_file)
        )
        self.start_training_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid weights for responsiveness
        webcam_window.grid_columnconfigure(0, weight=1)
        webcam_window.grid_columnconfigure(1, weight=3)

        webcam_window.focus_set()
        webcam_window.wait_window()
        self.root.deiconify()




    def show_image_feed_gui(self):
        self.root.withdraw()
        image_folder_window = ctk.CTkToplevel(self.root)
        image_folder_window.title('Image Feed Selection')
        image_folder_window.geometry('600x250')

        # Image Directory
        ctk.CTkLabel(image_folder_window, text='Select Image Directory:').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(image_folder_window, textvariable=folder_path_var, state='disabled')
        folder_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        browse_button = ctk.CTkButton(image_folder_window, text='Browse', command=lambda: self.browse_folder(folder_path_var))
        browse_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # Class Name
        ctk.CTkLabel(image_folder_window, text='Class Name:').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        class_name_var = tk.StringVar()
        class_name_entry = ctk.CTkEntry(image_folder_window, textvariable=class_name_var)
        class_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Start Processing Button
        start_processing_button = ctk.CTkButton(image_folder_window, text='Start Processing', command=lambda: self.start_image_processing(folder_path_var.get(), class_name_var.get()))
        start_processing_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # Start Training Button
        self.start_training_button = ctk.CTkButton(image_folder_window, text='Start Training', state='disabled', command=lambda: self.training_handler.start_training('gesture.csv'))
        self.start_training_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Configure grid weights for responsiveness
        image_folder_window.grid_columnconfigure(0, weight=1)
        image_folder_window.grid_columnconfigure(1, weight=3)
        image_folder_window.grid_columnconfigure(2, weight=1)

        image_folder_window.focus_set()
        image_folder_window.wait_window()
        self.root.deiconify()


    def start_webcam(self):
        class_name = self.file_name_var.get()
        camera_index = int(self.camera_index_var.get())  # Get the camera index from user input

        # Check if the camera index is valid
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            msgbox.showinfo(title='Error', message='Selected camera is not found or unavailable.')
            return
        cap.release()

        csv_file = 'gesture.csv'
        if class_name:
            self.root.withdraw()
            threading.Thread(target=self.main, args=(class_name, csv_file, camera_index)).start()
        else:
            msgbox.showinfo(title='Alert', message='Please enter a class name before starting')



    def start_image_processing(self, folder_path, class_name):
        csv_file = 'gesture.csv'
        if folder_path and class_name:
            processor = ImagePoseProcessor(self.start_training_button)  # Pass the button reference
            threading.Thread(target=processor.process_images_from_folder, args=(folder_path, class_name, csv_file)).start()
            # self.save_to_database(class_name)  # Save data to database here
        else:
            msgbox.showinfo(title='Alert', message=f'Please provide both an image directory and a class name.')
            print('Please provide both an image directory and a class name.')



    def main(self, class_name, csv_file, camera_index):
        cap = cv2.VideoCapture(camera_index)  # Use the specified camera index
        self.setup_window('Processing Webcam Feed')
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    msgbox.showinfo(title='Alert', message=f'Error: Could not read from webcam')
                    print('Error: Could not read from webcam')
                    break
                frame = self.process_frame(frame)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = holistic.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                self.draw_landmarks(image, results)
                self.export_landmarks_to_csv(results, class_name, csv_file)
                cv2.imshow('Processing Webcam Feed', image)
                if cv2.waitKey(10) & 255 == ord('q') or cv2.getWindowProperty('Processing Webcam Feed', cv2.WND_PROP_VISIBLE) < 1:
                    self.start_training_button.configure(state='normal')
                    break
        cap.release()
        cv2.destroyAllWindows()
        msgbox.showinfo(title='Processing Finished', message='Processed Finished. You can now train the new data.')
        print('Webcam processing finished.')

    def setup_window(self, window_name, width=1280, height=720):
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.resizeWindow(window_name, width, height)

    def process_frame(self, frame, target_width=1280):
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        new_height = int(target_width / aspect_ratio)
        return cv2.resize(frame, (target_width, new_height))

    def draw_landmarks(self, image, results):
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    def export_landmarks_to_csv(self, results, class_name, csv_file):
        if results.pose_landmarks:
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            pose_row.insert(0, class_name)
            try:
                with open(csv_file, mode='a', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(pose_row)
                    f.flush()
            except Exception as e:
                msgbox.showinfo(title='Alert', message=f'Error exporting data: {e}')
                print(f'Error exporting data: {e}')

    def close_webcam_gui(self, webcam_window):
        webcam_window.destroy()
        self.root.deiconify()

    def show_folder_gui(self):
        self.root.withdraw()
        folder_window = ctk.CTkToplevel(self.root)
        folder_window.title('Video Feed Selection')
        folder_window.geometry('600x250')  # Adjusted for better layout

        # Video Directory
        ctk.CTkLabel(folder_window, text='Select Video Directory:').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(folder_window, textvariable=folder_path_var, state='disabled')
        folder_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        browse_button = ctk.CTkButton(folder_window, text='Browse', command=lambda: self.browse_folder(folder_path_var))
        browse_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # Class Name
        ctk.CTkLabel(folder_window, text='Class Name:').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        class_name_var = tk.StringVar()
        class_name_entry = ctk.CTkEntry(folder_window, textvariable=class_name_var)
        class_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Start Processing Button
        start_processing_button = ctk.CTkButton(folder_window, text='Start Processing', command=lambda: self.start_video_processing(folder_path_var.get(), class_name_var.get(), folder_window))
        start_processing_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # Start Training Button
        self.start_training_button = ctk.CTkButton(folder_window, text='Start Training', state='disabled', command=lambda: self.training_handler.start_training('gesture.csv'))
        self.start_training_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Configure grid weights for responsiveness
        folder_window.grid_columnconfigure(0, weight=1)
        folder_window.grid_columnconfigure(1, weight=3)
        folder_window.grid_columnconfigure(2, weight=1)

        folder_window.focus_set()
        folder_window.wait_window()
        self.root.deiconify()



    def browse_folder(self, folder_path_var):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_path_var.set(folder_path)

    def start_video_processing(self, video_dir, class_name, folder_window):
        csv_file = 'gesture.csv'
        if video_dir and class_name:
            # Check for video files when 'Start Processing' is clicked
            video_files = [f for f in os.listdir(video_dir) if f.lower().endswith(('.mp4', '.avi'))]
            if video_files:
                # If video files are found, enable the Start Training button
                self.start_training_button.configure(state='normal')
                # Process the videos after enabling the training button
                processor = VideoPoseProcessor(video_dir, class_name, csv_file, self.start_training_button)
                threading.Thread(target=processor.process_videos).start()
                # self.save_to_database(class_name)  # Save data to database here
            else:
                msgbox.showinfo(title='Alert', message=f'No video files found in the folder.')
        else:
            msgbox.showinfo(title='Alert', message=f'Please provide both a video directory and a class name.')
            print('Please provide both a video directory and a class name.')



    def close_folder_gui(self, folder_window):
        folder_window.destroy()
        self.root.deiconify()

class TrainingHandler:

    def __init__(self):
        self.root = root
        self.fit_models = {}
        self.results_window = None

    def start_training(self, csv_file):
        df = pd.read_csv(csv_file)
        if 'class' in df.columns:
            X = df.drop('class', axis=1)
            y = df['class']
        else:
            y = df.iloc[:, 0]
            X = df.iloc[:, 1:]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
        pipelines = {'lr': make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, solver='lbfgs')), 'rc': make_pipeline(StandardScaler(), RidgeClassifier()), 'rf': make_pipeline(StandardScaler(), RandomForestClassifier()), 'gb': make_pipeline(StandardScaler(), GradientBoostingClassifier())}
        results = {}
        for algo, pipeline in pipelines.items():
            model = pipeline.fit(X_train, y_train)
            self.fit_models[algo] = model
            yhat = model.predict(X_test)
            score = accuracy_score(y_test, yhat)
            results[algo] = score
        self.show_results(results)

    def show_results(self, results):
        self.root.withdraw()
        self.results_window = ctk.CTkToplevel()
        self.results_window.title('Training Results')
        self.results_window.geometry('300x400')
        self.results_window.attributes('-topmost', 1)  # Ensure the window stays on top

        for algo, score in results.items():
            result_text = f'{algo}: {score:.2f}'
            ctk.CTkLabel(self.results_window, text=result_text).pack(pady=5)
            select_button = ctk.CTkButton(self.results_window, text='Select Algo', command=lambda a=algo: self.select_algorithm(a))
            select_button.pack(pady=5)

    def select_algorithm(self, algo):
        model = self.fit_models.get(algo)
        if model:
            file_path = filedialog.asksaveasfilename(defaultextension='.pkl', filetypes=[('Pickle files', '*.pkl'), ('All files', '*.*')], title=f'Save {algo} Model')
            if file_path:
                with open(file_path, 'wb') as f:
                    pickle.dump(model, f)
                print(f'{algo} model saved as {file_path}')
                msgbox.showinfo(title='Processing Finished', message=f'{algo} model saved as {file_path}')
                self.results_window.destroy()

class VideoPoseProcessor:

    def __init__(self, video_dir, class_name, csv_file, start_training_button):
        self.video_dir = video_dir
        self.class_name = class_name
        self.csv_file = csv_file
        self.start_training_button = start_training_button

    def process_videos(self):
        for filename in os.listdir(self.video_dir):
            if filename.endswith('.mp4') or filename.endswith('.avi'):
                video_path = os.path.join(self.video_dir, filename)
                self.process_video(video_path)
        print('Video processing finished. Now you can start training.')
        self.start_training_button.configure(state='normal')
        msgbox.showinfo(title='Processing Finished', message='Processing Finished. You can now train the new data.')

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = self.process_frame(frame)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = holistic.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                self.draw_landmarks(image, results)
                self.export_landmarks_to_csv(results, self.class_name)
                cv2.imshow('Processing Video', image)
                if cv2.waitKey(10) & 255 == ord('q'):
                    self.start_training_button.configure(state='normal')
                    break
        cap.release()
        cv2.destroyAllWindows()


    def process_frame(self, frame, target_width=1280):
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        new_height = int(target_width / aspect_ratio)
        return cv2.resize(frame, (target_width, new_height))

    def draw_landmarks(self, image, results):
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4), mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    def export_landmarks_to_csv(self, results, class_name):
        if results.pose_landmarks:
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            pose_row.insert(0, class_name)
            try:
                with open(self.csv_file, mode='a', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(pose_row)
                    f.flush()
            except Exception as e:
                msgbox.showinfo(title='Alert', message=f'Error exporting data: {e}')
                print(f'Error exporting data: {e}')


class ImagePoseProcessor:
    def __init__(self, start_training_button):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.start_training_button = start_training_button  # Store the reference to the button

    def process_images_from_folder(self, folder_path, class_name, csv_file):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Check if there are no image files
        if not image_files:
            msgbox.showinfo(title='Alert', message=f'No image files found in the folder.')
            print("No image files found in the folder.")
            self.start_training_button.configure(state='disabled')  # Disable start training button
            return
        
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Error: Could not read image {image_path}")
                    continue

                # Convert BGR to RGB for Mediapipe processing
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = holistic.process(image_rgb)

                # If pose landmarks are detected, export them to CSV
                if results.pose_landmarks:
                    self.export_landmarks_to_csv(results, class_name, csv_file)
                    self.draw_landmarks(image, results)

                # Display the processed image with landmarks
                cv2.imshow('Processed Image', image)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
        print("Finished processing images.")

        # After processing, enable the 'Start Training' button
        self.start_training_button.configure(state='normal')

    def draw_landmarks(self, image, results):
        """ Draw pose landmarks on the image """
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                self.mp_holistic.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

    def export_landmarks_to_csv(self, results, class_name, csv_file):
        """ Export pose landmarks to CSV, matching format in MotionFeedApp """
        if results.pose_landmarks:
            # Extract the landmarks from the results
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            # Insert the class name at the start of the row
            pose_row.insert(0, class_name)

            # Append to CSV file
            try:
                with open(csv_file, mode='a', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(pose_row)
                    f.flush()
            except Exception as e:
                msgbox.showinfo(title='Alert', message=f'Error exporting data: {e}')
                print(f'Error exporting data: {e}')



if __name__ == '__main__':
    root = ctk.CTk()
    app = MotionFeedApp(root)
    root.mainloop()