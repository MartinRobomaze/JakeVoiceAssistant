import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import pyjokes
import webbrowser
from PyQt5 import QtWidgets, QtGui
import sys
import newsScraper
import playsound


class Window(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super(Window, self).__init__(**kwargs)

        self.setWindowTitle("Jake voice assistant")
        self.init_gui()
        self.show()

    def init_gui(self):
        form = QtWidgets.QWidget()
        form_layout = QtWidgets.QVBoxLayout()
        form.setLayout(form_layout)

        box_layout = QtWidgets.QVBoxLayout()

        form_layout.addLayout(box_layout)

        background_image_label = QtWidgets.QLabel(self)
        background_image = QtGui.QPixmap('img/background.jpg')
        background_image_label.setPixmap(background_image)
        speak_button = QtWidgets.QPushButton("Speak", self)

        box_layout.addWidget(background_image_label)
        box_layout.addWidget(speak_button)

        self.setCentralWidget(form)

        speak_button.clicked.connect(main)


def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    tts.save("audio.mp3")
    playsound.playsound("audio.mp3")


def main():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print('Speak:')
        audio = r.listen(source)
        print('listening done')

    recognized_string = ""

    try:
        recognized_string = r.recognize_google(audio)
        print("You said " + recognized_string)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    if 'Jake' in recognized_string:
        if 'time' in recognized_string:
            time = datetime.now()
            time_string = "It's " + time.strftime("%H:%M")
            print(time_string)
            speak(time_string)
        elif 'find something about' in recognized_string:
            url = 'http://www.google.com/search?q=' + recognized_string[recognized_string.find("about ") + 6:]
            print(url)
            speak('This is what I found')
            webbrowser.open_new(url)
        elif 'play' in recognized_string:
            song = recognized_string[recognized_string.find('play') + 5:]

            for file in os.listdir("Music"):
                print(song)
                if song in file:
                    print(file)
        elif 'joke' in recognized_string:
            joke = str(pyjokes.get_joke())
            print(joke)
            speak(joke)
        elif 'Mamma Mia' in recognized_string:
            os.system("mpg321 MammaMia.mp3")
        elif 'Youtube' in recognized_string:
            url = 'https://www.youtube.com/results?search_query=' + recognized_string[recognized_string.find("about ") + 6:]
            print(url)
            speak('Opening Youtube')
            webbrowser.open_new(url)
        elif 'news' in recognized_string:
            news = newsScraper.get_latest_news()

            speak("These are today's biggest news.")

            for one_news in news:
                speak(one_news)


newsScraper = newsScraper.NewsScraper('https://inshorts.com/en/read')
application = QtWidgets.QApplication(sys.argv)
window = Window()
sys.exit(application.exec_())
