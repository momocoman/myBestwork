Virtual Keyboard with Hand Gesture and Voice Recognition

Description
This project demonstrates a Virtual Keyboard system that combines hand gesture recognition and voice input for text entry. Using computer vision, hand tracking, and speech recognition, the program allows users to interact with a virtual keyboard in an innovative way. Users can type by moving their fingers over keys displayed on the screen or by speaking into the microphone. The system leverages OpenCV, MediaPipe, and SpeechRecognition for an immersive user experience.
Virtual Keyboard with Hand Gesture and Voice Recognition
Description

    Hand Tracking and Gestures:

        Hand landmarks are detected, and gestures are used to interact with the virtual keyboard.

        Enables typing by "tapping" on virtual keys using fingertip positions.

    Voice-to-Text Input:

        Users can speak into the microphone, and the spoken words are converted into text.

        Allows seamless switching between gesture-based and voice-based typing.

    Dynamic Keyboard Layout:

        Virtual keys for letters, space, clear, backspace, and a special "Voice" button for speech recognition.

    Real-Time Feedback:

        Displays keypresses and recognized text in real time.

        Shows the frame rate (FPS) for performance monitoring.

Requirements

To run this project, you'll need the following dependencies:

    Python 3.6+

    OpenCV (pip install opencv-python)

    SpeechRecognition (pip install SpeechRecognition)

    MediaPipe (pip install mediapipe)

    Pynput (pip install pynput)

    A functional webcam for video capture.

    A microphone for voice input.

Usage

    Run the Script:

        Execute the Python script to launch the application.

    Hand Gesture Interaction:

        Use your index finger to "hover" over the virtual keys.

        Perform a gesture (e.g., tapping with the index and thumb together) to select a key.

    Voice Input:

        Activate the "Voice" button on the virtual keyboard by selecting it.

        Speak into the microphone to input text through speech recognition.

    Exit:

        Press the "Exit" button or close the application window to terminate.

How It Works

    Hand Tracking:

        Uses MediaPipe's Hand Tracking module to detect and track hand landmarks.

        Calculates the distance between the index finger and thumb to register a "click."

    Virtual Keyboard:

        A dynamic grid of keys is drawn using OpenCV, including letters, space, backspace, clear, and voice activation.

    Speech Recognition:

        SpeechRecognition library processes audio from the microphone.

        Converts recognized speech into text, which is appended to the virtual text box.

Potential Enhancements

    Add support for multilingual voice input.

    Include more sophisticated gesture-based navigation and control.

    Optimize for different screen resolutions and device capabilities.
