import customtkinter as ctk
import tkinter.messagebox as msgbox
from customtkinter import E, N, NE, NO, NORMAL, NS, ON, S, SE, TOP, W, X, Y
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import tkinter
import cv2
import mediapipe as mp
import numpy as npz
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
import time
ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

class MotionFeedApp:

    def __init__(self, root):
        self.root = root
        self.file_name_var = tk.StringVar()
        self.training_handler = TrainingHandler()
        self.setup_ui()

    def setup_ui(self):
        self.root.title('Motion Feed GUI')
        self.root.geometry('400x400')
        ctk.CTkLabel(self.root, text='Motion Feed', font=('Helvetica', 20)).pack(pady=10)
        ctk.CTkLabel(self.root, text='Choose an option you want to add a motion:').pack(pady=10)
        ctk.CTkButton(self.root, text='Via Live', command=self.show_webcam_gui).pack(pady=10)
        ctk.CTkButton(self.root, text='Via Folder', command=self.show_folder_gui).pack(pady=10)
        ctk.CTkButton(self.root, text='Via Image Feed', command=self.show_image_feed_gui).pack(pady=10)  # New button for image feed

    def upload_file(self):
        file = filedialog.askopenfile()
        if file:
            self.file_name_var.set(file.name)

    def enable_start_training_button(self):
        self.start_training_button.configure(state='normal')

    def show_webcam_gui(self):
        self.root.withdraw()
        webcam_window = ctk.CTkToplevel(self.root)
        webcam_window.title('Webcam Processing')
        webcam_window.geometry('400x250')
        ctk.CTkLabel(webcam_window, text='Class Name:').pack(pady=5)
        file_name_entry = ctk.CTkEntry(webcam_window, textvariable=self.file_name_var)
        file_name_entry.pack()
        ctk.CTkButton(webcam_window, text='Start Webcam', command=self.start_webcam).pack(pady=20)
        csv_file = 'gesture.csv'
        self.start_training_button = ctk.CTkButton(webcam_window, text='Start Training', state='disabled', command=lambda: self.training_handler.start_training('gesture.csv'))
        self.start_training_button.pack(pady=10)
        webcam_window.focus_set()
        webcam_window.wait_window()
        self.root.deiconify()

    def show_image_feed_gui(self):
        self.root.withdraw()
        image_folder_window = ctk.CTkToplevel(self.root)
        image_folder_window.title('Image Folder Selection')
        image_folder_window.geometry('400x350')
        
        ctk.CTkLabel(image_folder_window, text='Select Image Directory:').pack(pady=5)
        folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(image_folder_window, textvariable=folder_path_var, state='disabled')
        folder_entry.pack(pady=5)
        ctk.CTkButton(image_folder_window, text='Browse', command=lambda: self.browse_folder(folder_path_var)).pack(pady=5)
        
        ctk.CTkLabel(image_folder_window, text='Class Name:').pack(pady=5)
        class_name_var = tk.StringVar()
        class_name_entry = ctk.CTkEntry(image_folder_window, textvariable=class_name_var)
        class_name_entry.pack(pady=5)
        
        ctk.CTkButton(image_folder_window, text='Start Processing', command=lambda: self.start_image_processing(folder_path_var.get(), class_name_var.get())).pack(pady=20)

        self.start_training_button = ctk.CTkButton(image_folder_window, text='Start Training', state='disabled', command=lambda: self.training_handler.start_training('gesture.csv'))
        self.start_training_button.pack(pady=10)
        
        image_folder_window.focus_set()
        image_folder_window.wait_window()
        self.root.deiconify()

    def start_webcam(self):
        class_name = self.file_name_var.get()
        csv_file = 'gesture.csv'
        if class_name:
            self.root.withdraw()
            threading.Thread(target=self.main, args=(class_name, csv_file)).start()
        else:
            msgbox.showinfo(title='Alert', message=f'Please enter a class name before starting')
            print('Please enter a class name before starting.')

    def start_image_processing(self, folder_path, class_name):
        csv_file = 'gesture.csv'
        if folder_path and class_name:
            processor = ImagePoseProcessor()
            threading.Thread(target=processor.process_images_from_folder, args=(folder_path, class_name, csv_file)).start()
            self.start_training_button.configure(state='normal')
        else:
            msgbox.showinfo(title='Alert', message=f'Please provide both an image directory and a class name.')
            print('Please provide both an image directory and a class name.')

    def main(self, class_name, csv_file):
        cap = cv2.VideoCapture(0)
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
        folder_window.title('Folder Selection')
        folder_window.geometry('400x350')
        ctk.CTkLabel(folder_window, text='Select Video Directory:').pack(pady=5)
        folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(folder_window, textvariable=folder_path_var, state='disabled')
        folder_entry.pack(pady=5)
        ctk.CTkButton(folder_window, text='Browse', command=lambda: self.browse_folder(folder_path_var)).pack(pady=5)
        ctk.CTkLabel(folder_window, text='Class Name:').pack(pady=5)
        class_name_var = tk.StringVar()
        class_name_entry = ctk.CTkEntry(folder_window, textvariable=class_name_var)
        class_name_entry.pack(pady=5)
        ctk.CTkButton(folder_window, text='Start Processing', command=lambda: self.start_video_processing(folder_path_var.get(), class_name_var.get(), self.start_training_button)).pack(pady=20)

        self.start_training_button = ctk.CTkButton(folder_window, text='Start Training', state='disabled', command=lambda: self.training_handler.start_training('gesture.csv'))
        self.start_training_button.pack(pady=10)
        folder_window.focus_set()
        folder_window.wait_window()
        self.root.deiconify()


    def browse_folder(self, folder_path_var):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_path_var.set(folder_path)

    def start_video_processing(self, video_dir, class_name, start_training_button):
        csv_file = 'gesture.csv'
        if video_dir and class_name:
            processor = VideoPoseProcessor(video_dir, class_name, csv_file, start_training_button)
            threading.Thread(target=processor.process_videos).start()
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
        self.results_window.geometry('300x300')
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
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils

    def process_images_from_folder(self, folder_path, class_name, csv_file):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            print("No image files found in the folder.")
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