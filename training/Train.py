from PIL import Image, ImageTk
from tkinter import Tk, Label, LabelFrame, Button, StringVar, OptionMenu, Frame, filedialog, Text
import cv2 as cv2
import mediapipe as mp
import numpy as np
import os
import datetime as dt

'''

Global variables

'''
trainer_id = 'guest'
is_capturing_data = False
video_device_index = 0
data_path = os.path.expanduser('~/Documents/')
word_array = []
timestamp = dt.datetime.now().strftime("%m.%d.%y_%H.%M")
path_id = '{}_{}'.format(trainer_id, timestamp)
no_sequences = 30
sequence_length = 30

'''

Set up Tkinter logic

'''


def return_camera_indexes():
    index = -1
    arr = []
    i = 10
    while i >= 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


def start_data_capture():
    global is_capturing_data
    global trainer_id
    is_capturing_data = not is_capturing_data
    id_input = id_txt.get("1.0", "end-1c")
    if not id_input == '':
        trainer_id = id_input

    cap = cv2.VideoCapture(video_device_index)
    with mp_holistic.Holistic(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5) as holistic:
        # Loop through actions
        for action in word_array:
            # Loop through sequences aka videos
            for sequence in range(no_sequences):
                # Loop through video length aka sequence length
                for frame_num in range(sequence_length):

                    ret, frame = cap.read()

                    # Prep image for MediaPipe
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = cv2.flip(image, 1)
                    image.flags.writeable = False
                    results = holistic.process(image)

                    # Start drawing annotations and interpreting results
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Draw landmarks on screen
                    draw_training_landmarks(image, results)

                    # NEW Apply wait logic
                    if frame_num == 0:
                        # Generate screen text
                        window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        cv2.putText(image, 'PREPARE TO CAPTURE: {}'.format(action),
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 5, cv2.LINE_AA)
                        cv2.putText(image, 'PREPARE TO CAPTURE: {}'.format(action),
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.putText(image, 'Sequence {}'.format(sequence),
                                    (25, int(window_height) - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                        cv2.putText(image, 'Sequence {}'.format(sequence),
                                    (25, int(window_height) - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

                        # Show to screen
                        tkinter_image = ImageTk.PhotoImage(
                            Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
                        L1['image'] = tkinter_image
                        root.update()

                        # have the sign take 2 seconds to complete
                        cv2.waitKey(2000)
                    else:
                        # Generate screen text
                        window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        cv2.putText(image, action,
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 5, cv2.LINE_AA)
                        cv2.putText(image, action,
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.putText(image, 'Sequence {}'.format(sequence),
                                    (25, int(window_height) - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                        cv2.putText(image, 'Sequence {}'.format(sequence),
                                    (25, int(window_height) - 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

                        tkinter_image = ImageTk.PhotoImage(
                            Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
                        L1['image'] = tkinter_image
                        root.update()

                    # NEW Export keypoints
                    keypoints = extract_keypoints(results)

                    npy_path = os.path.join(
                        data_path, 'SignTraining', action, path_id, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)

                    # Close the window with keyboard interrupt of 'Q'
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
    cap.release()


def set_video_device(new_index):
    global video_device_index
    video_device_index = new_index


def browseFiles():
    directory_name = filedialog.askdirectory(initialdir=os.path.expanduser(
        '~/Documents'), title="Select a Save Directory")
    label_file_explorer.configure(text="Directory Selected: " + directory_name)
    global data_path
    data_path = directory_name


def generateWordDirectories():
    global word_array
    words_string = input_txt.get("1.0", "end-1c")
    if not words_string == '':
        word_array = words_string.split(",")
        button_text.configure(
            text='{} words confirmed!'.format(len(word_array)))

        for word in word_array:
            for sequence in range(no_sequences):
                try:
                    os.makedirs(os.path.join(
                        data_path, 'SignTraining', word, path_id, str(sequence)))
                except:
                    pass


root = Tk()
root.title('Sign Training')

# Horizontal Options Container
options_container = Frame(root)
options_container.grid(sticky="we")
options_container.grid_rowconfigure(0, weight=1)
options_container.grid_columnconfigure(0, weight=1)

# Capture Device Menu
capture_device_container = Frame(options_container)
capture_device_container.grid(row=0)
cap_option_title = Label(capture_device_container,
                         text='Select Video Input:', fg='blue')
cap_option_title.grid(row=0, column=0, padx=10, pady=10)
cap = cv2.VideoCapture(video_device_index)
cap_option = StringVar(options_container)
cap_option.set(video_device_index)
cap_menu = OptionMenu(capture_device_container,
                      cap_option, *return_camera_indexes())
cap_menu.grid(row=0, column=1, padx=10, pady=10)

# Directory Selector Container
directory_container = Frame(options_container)
directory_container.grid(row=1)
label_file_explorer = Label(
    directory_container, text="Select Save Directory:", fg='blue')
button_explore = Button(directory_container,
                        text="Browse Files", command=browseFiles)
label_file_explorer.grid(row=0, column=0, padx=10, pady=10)
button_explore.grid(row=0, column=1, padx=10, pady=10)

# Word Input and Conversion into array
word_input_container = Frame(options_container)
word_input_container.grid(row=2)
label_text_array = Label(
    word_input_container, text="Enter words to train (with format: word1,word2,word3):", fg='blue')
label_text_array.grid(row=0, column=0, padx=10, pady=10)
input_txt = Text(word_input_container, bg='light grey', height=2, width=20)
input_txt.grid(row=0, column=1, padx=10, pady=10)
button_text = Button(word_input_container,
                     text='Confirm Words', command=generateWordDirectories)
button_text.grid(row=0, column=2, padx=10, pady=10)

# Start Capture Button
capture_container = Frame(options_container)
capture_container.grid(row=3)
id_label = Label(capture_container, text="Enter your name:", fg='blue')
id_label.grid(row=0, column=0, padx=10, pady=10)
id_txt = Text(capture_container, bg='light grey', height=1, width=10)
id_txt.grid(row=0, column=1, padx=10, pady=10)
b = Button(capture_container, text='Start Capturing Data',
           fg='red', command=start_data_capture)
b.grid(row=0, column=2, padx=10, pady=10)

options_container.pack(fill='x', anchor='center')

# Video Stream Container
tk_height = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
tk_width = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
f1 = LabelFrame(root)
f1.pack()
L1 = Label(f1)
L1.pack()

'''

Load ML model and MediaPipe landmarks

'''

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten(
    ) if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten(
    ) if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten(
    ) if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten(
    ) if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(
        255, 0, 0), thickness=2, circle_radius=1), mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(
        0, 255, 0), thickness=2, circle_radius=1), mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(
        color=(0, 0, 255), thickness=2, circle_radius=1), mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(
        color=(0, 0, 255), thickness=2, circle_radius=1), mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1))


def draw_training_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(
        0, 0, 0), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(
        0, 0, 0), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(
        color=(0, 0, 0), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing.DrawingSpec(
        color=(0, 0, 0), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1))


'''

Video capture and analysis

'''

with mp_holistic.Holistic(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.5) as holistic:
    while cap.isOpened() and not is_capturing_data:
        ret, frame = cap.read()

        # Prep image for MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = holistic.process(image)

        # Start drawing annotations and interpreting results
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw landmarks on screen
        draw_landmarks(image, results)

        # Generate screen text
        window_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cv2.putText(image, 'Preview (Make sure landmarks are initialized)',
                    (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5, cv2.LINE_AA)
        cv2.putText(image, 'Preview (Make sure landmarks are initialized)',
                    (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        tkinter_image = ImageTk.PhotoImage(
            Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        L1['image'] = tkinter_image

        root.update()

        # Close the window with keyboard interrupt of 'Q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
