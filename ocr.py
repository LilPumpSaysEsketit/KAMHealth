import tkinter as tk
import os
import cv2
import eel
import sys
import time
from PIL import Image, ImageTk
import numpy
import pytesseract
eel.init('web')

@eel.expose
def snap():
    def pictureTaker():
        global cancel, camera, prevImg, button, button1, camIndex, cap, capHeight, capWidth, fileName
        fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
        cancel = False

        def prompt_ok(event = 0):
            global cancel, button, button1
            cancel = True

            button.place_forget()
            #button1 = tk.Button(mainWindow, text="Good Image!", command=saveAndExit)
            #button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
            #button1.focus()
            saveAndExit(0)

        def saveAndExit(event = 0):
            global prevImg

            if (len(sys.argv) < 2):
                filepath = "imageCap.png"
            else:
                filepath = sys.argv[1]

            prevImg.save(filepath)
            mainWindow.quit()

        def changeCam(event=0, nextCam=-1):
            global camIndex, cap, fileName

            if nextCam == -1:
                camIndex += 1
            else:
                camIndex = nextCam
            del(cap)
            cap = cv2.VideoCapture(camIndex)

            #try to get a frame, if it returns nothing
            success, frame = cap.read()
            if not success:
                camIndex = 1
                del(cap)
                cap = cv2.VideoCapture(camIndex)

            f = open(fileName, 'w')
            f.write(str(camIndex))
            f.close()

        try:
            f = open(fileName, 'r')
            camIndex = int(f.readline())
        except:
            camIndex = 0

        cap = cv2.VideoCapture(camIndex)
        capWidth = cap.get(3)
        capHeight = cap.get(4)

        success, frame = cap.read()
        if not success:
            if camIndex == 0:
                print("Error, No webcam found!")
                sys.exit(1)
            else:
                changeCam(nextCam=0)
                success, frame = cap.read()
                if not success:
                    print("Error, No webcam found!")
                    sys.exit(1)


        mainWindow = tk.Tk(screenName="Camera Capture")
        mainWindow.resizable(width=False, height=False)
        mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
        lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
        button = tk.Button(mainWindow, text="Capture", command=prompt_ok)
        button_changeCam = tk.Button(mainWindow, text="Switch Camera", command=changeCam)

        lmain.pack()
        button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
        button.focus()
        button_changeCam.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)

        def show_frame():
            global cancel, prevImg, button

            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            prevImg = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=prevImg)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            if not cancel:
                lmain.after(10, show_frame)

        show_frame()
        mainWindow.mainloop()
        pull_text()

    def pull_text():
        global arrayfirst, arraysecond
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\spaze\AppData\Local\Tesseract-OCR\tesseract.exe"

        file = Image.open("imageCap.png")
        string = pytesseract.image_to_string(file, lang='eng')
        array = string.split()
        r = 0
        h = 1
        i = len(array)/2
        p = i
        arrayfirst = []
        arraysecond = []
        while i > 0:
            arrayfirst.append(array[r])
            r += 2
            i -= 1
        while p > 0:
            arraysecond.append(array[h])
            h += 2
            p -= 1

    pictureTaker()

eel.start('food.html')

#https://raw.githubusercontent.com/AshbyGeek/EasyWebcamCamera/master/cap.py