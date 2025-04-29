import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from tensorflow.keras.layers import DepthwiseConv2D
import serial
import time
# Configure the serial port
# MacOS looks somethinglike this: "/dev/ttyUSB0"
port = "COM8"  # Replace with your serial port
baud_rate = 9600
arduino = serial.Serial(port, baud_rate)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Custom layer for DepthwiseConv2D
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # Ignore 'groups' argument
        super().__init__(*args, **kwargs)

# Load the model
model = load_model("keras_Model.h5", compile=False, custom_objects={"DepthwiseConv2D": CustomDepthwiseConv2D})

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
vid = cv2.VideoCapture(0)
try:
    while True:
        # Grab the webcamera's image.
        ret, image = vid.read()

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score

        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        if class_name == "0 Human\n":
            message_to_send = "Red\n"
        elif class_name == "1 Dog\n":
            message_to_send = "Green\n"
            
        else:
            message_to_send = "Blank\n"

        arduino.write(message_to_send.encode('utf-8'))
        arduino.flush()
          # Small delay for stability
        if (class_name == "1 Dog\n"):
            time.sleep(30)
        else:
            time.sleep(0.2)
        # Read response from Arduino
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').strip()
            print(f"Received: {received_data}")


        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break
except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    arduino.close()
    print("Serial port closed")
    vid.release()
    cv2.destroyAllWindows()
