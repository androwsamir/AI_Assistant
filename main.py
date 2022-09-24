import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import requests
import json
import webbrowser
import os
import pywhatkit as kit
import flask
import sys
import smtplib
import clipboard
import pyautogui
import pyjokes
import time
from time import sleep
import subprocess
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import cv2
#from Jarvis.features.gui import *
#from Jarvis import config
#import wolframalpha

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')

#print(voices)
engine.setProperty('voice',voices[0].id)

author = "Andrew"

camera_port = 0
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)

#====================================Momery=====================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'atharvaaingle@gmail.com',
    'my official email': 'atharvaaingle@gmail.com',
    'my second email': 'atharvaaingle@gmail.com',
    'my official mail': 'atharvaaingle@gmail.com',
    'my second mail': 'atharvaaingle@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

#===============================================================================

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#===============================================================================
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('anrowsamir2019@gmail.com','01555498221%ASI')
    server.sendmail('anrowsamir2019@gmail.com',to,content)
    server.close()
#===============================================================================
def wishMe():
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Good Morning {author}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon {author}")
    else:
        speak(f"Good Evening {author}")
    c_time = datetime.datetime.now().strftime("%I:%M")
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
#===============================================================================
def takeCommand():
    '''
    take microphone input from the user and return string
    '''
    
    r = sr.Recognizer()
    with sr.Microphone(device_index = 2) as source:
        print("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-EG')
        print(f"User Said:{query} \n")
    except Exception as e:
        print(f"Sorry {author}, Say That again... ")
        return takeCommand()
    return query
#===============================================================================
def getnews(query):
    speak("News Headlines")
    query = query.replace("news","")
    url = "https://newsapi.org/v2/top-headlines?country=eg&apiKey=e61479883ee54055adbe415994cee4eb"
    news = requests.get(url).text
    news = json.loads(news)
    art = news['articles']
    for article in art:
        print(article['title'])
        speak(article['title'])

        print(article['description'])
        speak(article['description'])
        speak("Moving on to the next news")
#===============================================================================
def whatsmsg():
    speak("Who do you want to send the message?")
    number = input("Enter number : \n")
    speak("What do you want to send?")
    msg = input("Enter the message : ")
    speak("please Enter Time sir.")
    H = int(input("Enter Hour?\n"))
    M = int(input("Enter Minutes?\n"))
    kit.sendwhatmsg(number, msg, H,M)
#===============================================================================
def weather():
    city = "Giza"
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=16f0afad2fd9e18b7aee9582e8ce650b&units=metric").json()
    temp1 = res["weather"][0]["description"]
    temp2 = res["main"]["temp"]
    speak(
        f"Temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}")
#===============================================================================
def getinfo(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia","")
    results = wikipedia.summary(query, sentences = 2)
    speak("According to wikipedia")
    print(results)
    speak(results)
#===============================================================================
def get_image():
    retval, im = camera.read()
    return im
#===============================================================================
def main():
    while True:
        query = takeCommand().lower()
        if 'wikipedia' and 'who' in query:
            getinfo(query)

        elif 'time' in query:
            speak("Current time is " +
                  datetime.datetime.now().strftime("%I:%M"))

        elif 'date' in query:
            speak("Today is " + str(datetime.datetime.now().day)
                  + " " + str(datetime.datetime.now().month)
                  + " " + str(datetime.datetime.now().year))

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            assname = query
 
        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            assname = takeCommand()
            speak("Thanks for naming me")
        
        elif 'news' in query:
            getnews(query)

        elif 'open google' in query:
            speak('Opening Google')
            webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s').open("google.com")

        elif 'open youtube' in query:
            speak('Opening Youtube')
            webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s').open("youtube.com")

        elif 'search' in query:
            speak("What should i search?")
            um = takeCommand().lower()
            speak('Got It')
            webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s').open(f"{um}")

        elif 'ip address' in query:
            ip = requests.get('http://api.ipify.org').text
            print(f"Your ip is {ip}")
            speak(f"Your ip is {ip}")

        elif 'weather' in query:
            weather()

        elif 'open cmd' in query:
            os.system("start cmd")

        elif 'code' in query:
            codepath = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\devenv.exe"
            os.startfile(codepath)

        elif 'play music' in query:
            music_dir =  'B:\\ASI\\06-Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'play youtube' in query:
            speak('What should i search in youtube?')
            cm = input("Enter what should i search for : ")
            kit.playonyt(f"{cm}")

        elif 'send a message' in query:
            whatsmsg()

        elif 'send email' in query:
            speak("What should i send sir?")
            content = takeCommand().lower()
            speak("Whom to send the email , enter email address sir")
            to = input("Enter Email Address : ")
            sendEmail(to,content)

        elif 'read' in query:
            speak("you copied that")
            speak(clipboard.paste())

        elif 'joke' in query:
            speak("I have a good one")
            speak(pyjokes.get_joke())

        elif 'screenshot' in query:
            speak("I will take a screenshot")
            pyautogui.screenshot(str(time.time()) + ".png").show()

        elif "camera" in query or "take a photo" in query:
            cv2.namedWindow("Python Webcam Screenshot App")
            img_counter = 0
            while True:
                ret,frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test",frame)
                k = cv2.waitKey(1)
                if k%256 == 27:
                    print("Escape hit, closing the app")
                    break
                elif k%256 == 32:
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name,frame)
                    print("screenshot taken")
                    img_counter += 1
            cam.release()
            cv2.destroyAllWindows()
            #====Anter way=====
            
            #for i in range(ramp_frames):
            #    temp = get_image()
            #print("Capturing Face...")
            #camera_capture = get_image()
            #file = ("test_image.png")
            #cv2.imwrite(file,camera_capture)

        
            
        elif 'open stackoverflow' in query:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'ask' in query:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="XJHK9V-PPG4XW752Q"
            client = wolframalpha.Client('XJHK9V-PPG4XW752Q')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif 'lock window' in query or 'close window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
 
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
                 
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif 'log off' in query or 'sign out' in query:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(input("Enter how much time in sec i will stop listening : "))
            time.sleep(a)
            print(a)
        
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")
        
        elif 'who are you' in query or 'what can you do' in query:
            speak('I am Jarvis version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of Egypt and you can ask me computational or geographical questions too!')

        elif "how are you" in query:
            speak("I'm fine, glad you me that")
            
        elif "write a note" in query:
            speak("What should i write, sir")
            note = input("Enter the note : ")
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
         
        elif "show me note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif 'goodbye' in query or 'ok bye' in query or 'stop' in query:
           speak(f"Good bye {author}")
           return
        
        elif 'who made you' in query or 'who created you' in query or 'who discovered you' in query:
        
           speak(f"I was built by {author}")
           print(f"I was built by {author}")

        else:
           main()
        
if __name__ == "__main__":
    clear = lambda: os.system('cls')

    clear()
    wishMe()
    main()