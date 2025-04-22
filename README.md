# Python-Arduino-DogDoor-Recognition
IT 254 Project 2

Project Steps:

1) train facial recognition model
- Accessed teachable machine at https://teachablemachine.withgoogle.com/train.
- Trained the model to recognize between images showing a Dog, a human face and images that show neither.
- Exported the model in Keras format.

2) Upload Arduino Code:
- Opened the Arduino IDE and uploaded the attached code.
- The attached code should inform the Arduino to light up different lights if it sees a human, a dog or nothing.
- If a Dog is detected the Aurduino will activate the Servo motor to unlock a dog door

3) Set up Arduino Python Connection
- Open Visual Studio Code and input the attached Python code.
- The attached code should reference the Keras model and labels and provide the appropriate input to the Arduino when a dog or a human face is being seen by the computer camera.

4) Test System
- Close the Arduino IDE.
- Activate the code on Visual Studio Code.
- Everything is working correctly if the camera sees a dog and the LED lights up and activates the servo.

Systems used:
- Python 3
- TensorFlow
- Keras
- OpenCV
- PySerial
- Arduino IDE
- Arduino Mega 2560


Video Example:
