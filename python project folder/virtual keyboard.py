import cv2
import numpy as np
import time
import speech_recognition as sr
import threading
from keys import *
from handTracker import *
from pynput.keyboard import Controller


def getMousePos(event, x, y, flags, param):
    global clickedX, clickedY, mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
        mouseX, mouseY = x, y


def calculateIntDistance(pt1, pt2):
    return int(((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5)


# Create keys
w, h = 80, 60
startX, startY = 40, 200
keys = []
letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")

for i, l in enumerate(letters):
    if i < 10:
        keys.append(Key(startX + i * w + i * 5, startY, w, h, l))
    elif i < 19:
        keys.append(Key(startX + (i - 10) * w + i * 5, startY + h + 5, w, h, l))
    else:
        keys.append(Key(startX + (i - 19) * w + i * 5, startY + 2 * h + 10, w, h, l))

keys.append(Key(startX + 25, startY + 3 * h + 15, 5 * w, h, "Space"))
keys.append(Key(startX + 8 * w + 50, startY + 2 * h + 10, w, h, "clr"))
keys.append(Key(startX + 5 * w + 30, startY + 3 * h + 15, 5 * w, h, "<--"))

# New "Voice" button for speech recognition in the lower-right corner
voiceKey = Key(startX + 9 * w + 100, startY + 5 * h + 15, w, h, "Voice")

showKey = Key(300, 5, 80, 50, 'Show')
exitKey = Key(300, 65, 80, 50, 'Exit')
textBox = Key(startX, startY - h - 5, 10 * w + 9 * 5, h, '')

cap = cv2.VideoCapture(0)
ptime = 0

tracker = HandTracker(detectionCon=1)

frameHeight, frameWidth, _ = cap.read()[1].shape
showKey.x = int(frameWidth * 1.5) - 85
exitKey.x = int(frameWidth * 1.5) - 85

clickedX, clickedY = 0, 0
mouseX, mouseY = 0, 0

show = False
cv2.namedWindow('video')
counter = 0
previousClick = 0

keyboard = Controller()

# Speech Recognizer
recognizer = sr.Recognizer()


def voice_to_text():
    """Runs voice recognition in a separate thread to avoid blocking."""

    def recognize_speech():
        with sr.Microphone() as source:
            print("Voice mode active... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                # Keep listening until interrupted or the program ends
                while True:
                    print("Listening...")
                    audio = recognizer.listen(source)  # Listen indefinitely
                    try:
                        # Process and recognize speech
                        text = recognizer.recognize_google(audio, language="en")  # Arabic recognition
                        print(f"You said: {text}")
                        textBox.text += " " + text  # Append recognized speech to text box
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError:
                        print("Error connecting to Google Speech Recognition service")
            except KeyboardInterrupt:
                print("Voice recognition stopped")

    threading.Thread(target=recognize_speech, daemon=True).start()



while True:
    if counter > 0:
        counter -= 1

    signTipX = signTipY = thumbTipX = thumbTipY = 0

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (int(frameWidth * 1.5), int(frameHeight * 1.5)))
    frame = cv2.flip(frame, 1)
    frame = tracker.findHands(frame)
    lmList = tracker.getPostion(frame, draw=False)

    if lmList:
        signTipX, signTipY = lmList[8][1], lmList[8][2]
        thumbTipX, thumbTipY = lmList[4][1], lmList[4][2]

        if calculateIntDistance((signTipX, signTipY), (thumbTipX, thumbTipY)) < 50:
            centerX = (signTipX + thumbTipX) // 2
            centerY = (signTipY + thumbTipY) // 2
            cv2.line(frame, (signTipX, signTipY), (thumbTipX, thumbTipY), (0, 255, 0), 2)
            cv2.circle(frame, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = int(1 / (ctime - ptime))

    cv2.putText(frame, f"{fps} FPS", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    showKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)
    exitKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)
    cv2.setMouseCallback('video', getMousePos)

    if showKey.isOver(clickedX, clickedY):
        show = not show
        showKey.text = "Hide" if show else "Show"
        clickedX, clickedY = 0, 0

    if exitKey.isOver(clickedX, clickedY):
        exit()

    alpha = 0.5
    if show:
        textBox.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.3)
        for k in keys + [voiceKey]:  # Include the Voice button in key processing
            if k.isOver(mouseX, mouseY) or k.isOver(signTipX, signTipY):
                alpha = 0.1

                if k.isOver(clickedX, clickedY):
                    if k.text == '<--':
                        textBox.text = textBox.text[:-1]
                    elif k.text == 'clr':
                        textBox.text = ''
                    elif k.text == "Voice":
                        voice_to_text()  # Activate voice recognition
                    elif len(textBox.text) < 30:
                        textBox.text += " " if k.text == "Space" else k.text

                if k.isOver(thumbTipX, thumbTipY):
                    clickTime = time.time()
                    if clickTime - previousClick > 0.4:
                        if k.text == '<--':
                            textBox.text = textBox.text[:-1]
                        elif k.text == 'clr':
                            textBox.text = ''
                        elif k.text == "Voice":
                            voice_to_text()
                        elif len(textBox.text) < 30:
                            textBox.text += " " if k.text == "Space" else k.text
                            keyboard.press(k.text)
                        previousClick = clickTime
            k.drawKey(frame, (255, 255, 255), (0, 0, 0), alpha=alpha)
            alpha = 0.5
        clickedX, clickedY = 0, 0

    ptime = ctime
    cv2.imshow('video', frame)

    if cv2.waitKey(1) == ord('1'):
        break

cap.release()
cv2.destroyAllWindows()