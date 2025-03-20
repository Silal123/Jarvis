import vosk
import pyaudio
import json
import signal
import os
import exeutils as ExeUtils
from PIL import ImageGrab, Image
from datetime import datetime
from plyer import notification

import webbrowser
import subprocess, sys
from subprocess import Popen, PIPE

import pyttsx3

import logger as Logger

Logger.info("Loading Projekt...")

#############################################
def signal_handler(signal, frame):
    for f in os.listdir("tmp"):
        os.remove(os.path.join("tmp", f))
    Logger.warning("Exiting!")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
#############################################

for f in os.listdir("tmp"):
    os.remove(os.path.join("tmp", f))

engine = pyttsx3.init()

Logger.info("Loading Model")
model = vosk.Model(r"vosk-model-de-0.21")
Logger.success(f"Loaded Model {model}")

Logger.info("Loading Recognizer")
recognizer = vosk.KaldiRecognizer(model, 16000)
Logger.success("Loaded Recognizer")

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
Logger.success("Started Mic Stream")

jarvis_words = ["jarvves", "jarvis", "jarvas", "jarfes", "jahwes", "davis", "jahwe", "yaris"]
chatbot_names = ["chatgbt", "chat chip it", "jetski pitti", "jetski bitte"]
known_apps = [
    (("chrome", "google chrome", "browser"), r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    #(("cmd", "c m d", "eingabeaufforderung", "console"), r"C:\Windows\system32\cmd.exe"),
    (("explorer", "files", "dateien", "datei explorer"), r"explorer.exe"),
    (("steam"), r"C:\Program Files (x86)\Steam\steam.exe"),
    (("java", r"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.1.4\bin\idea64.exe")),
    (("editor"), r"C:\Users\silas\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
    (("discord", "disco"), r"C:\Users\silas\AppData\Local\Discord\Update.exe"),
    (("content warning"), r"C:\Program Files (x86)\Steam\steamapps\common\Content Warning\Content Warning.exe"),
    (("terraria"), r"C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe")
    #(("laby", "labymod", "laby", "levy", "labbi mod", "labby mott", "levy mott", "levi mott"), r"C:\Users\silas\AppData\Local\labymodlauncher\LabyModLauncher.exe"),
    #(("minecraft", "minecraft louncher", "minecraft launcher", "mein craft launcher", "mein kraft launcher"), r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe")
]
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(r"C:\Program Files\Google\Chrome\Application\chrome.exe"))


def start_chatgbt(text: list):
    print("chatbot")
    print(str(text))

def say(text: str):
    engine.say(text)
    engine.runAndWait()

def notify(title: str, message: str, app_icon="./icons/icon2.ico"):
    notification.notify(
        title = title,
        message = message,
        timeout = 10,
        app_name = "Jarvis",
        app_icon = app_icon,
    )


last_screens = []

notify("Started successful!", "Now listening to your voice")
Logger.warning("Starting Vosk Listening")
while True:
    data = stream.read(1024, exception_on_overflow=False)
    ask_jarvis = False
    jarvis_quest = []

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        text = text[14:-3] # Format the Text!
        print(text)

        for word in text.split(' '):
            if ask_jarvis:
                jarvis_quest.append(word)
                continue
            if word.lower() in jarvis_words:
                Logger.warning("Jarvis was Called!")
                ask_jarvis = True
        
        if len(jarvis_quest) > 0:
            if jarvis_quest[0] in ["öffne", "öffnet", "öffnen", "öffner"] and len(jarvis_quest) > 1:
                if jarvis_quest[1] in ["den"] and len(jarvis_quest) > 2:
                    if jarvis_quest[2] in ["letzten", "vorletzten"] and len(jarvis_quest) > 3:
                        if jarvis_quest[3] in ["screenshot"]:
                            if jarvis_quest[2] == "letzten": back = 1
                            if jarvis_quest[2] == "vorletzten": back = 2
                            if len(last_screens) == 0 + back - 1:
                                Logger.warning("No Screenshot found")
                                continue
                        im = Image.open("screenshots/" + str(last_screens[len(last_screens)-back]))
                        im.show()
                        continue


            if jarvis_quest[0] in ["mache", "mach"] and len(jarvis_quest) > 1:
                if jarvis_quest[1] in ["einen"] and len(jarvis_quest) > 2:
                    make = jarvis_quest[2:]
                    make_name = " ".join(make)

                    if make_name in ["screenshot"]:
                        screenshot = ImageGrab.grab()
                        now = datetime.now()

                        if not os.path.exists(os.path.join("screenshots")): os.mkdir("screenshots")
                        screen_name = f"screenshot-{now.strftime("%Y_%m_%d-%H_%M_%S")}.png"
                        screenshot.save("screenshots/" + screen_name)

                        #im = Image.open("screenshots/" + screen_name)
                        #im.show()
                        last_screens.append(screen_name)
                        screenshot.close()

                        if not os.path.exists(os.path.join("tmp")): os.mkdir("tmp")
                        screen_ico = Image.open("screenshots/" + screen_name)
                        screen_ico.save("tmp/" + screen_name + ".ico", format="ICO")

                        notify(f"Made Screenshot", f"Screenshot saved to {screen_name}!", app_icon="tmp/" + screen_name + ".ico")
                        #os.remove("tmp/" + screen_name + ".ico")

                        Logger.success(f"Saved Screenshot {screen_name}")
                continue

            if jarvis_quest[0] in ["lösche", "löschen"] and len(jarvis_quest) > 1:
                if jarvis_quest[1] in ["alle"] and len(jarvis_quest) > 2:
                    if jarvis_quest[2] in ["screenshots"]:
                        #os.remove("screenshots")
                        notify("Screenshots Cleared", "All screenshots deleted!", app_icon="icons/yes.ico")
                        continue




            if jarvis_quest[0] in ["suche"] and len(jarvis_quest) > 1:
                search = jarvis_quest[1:]
                if jarvis_quest[1] in ["nach"]:
                    search = jarvis_quest[2:]

                search = str(" ".join(search))

                webbrowser.get('chrome').open(f"https://www.google.com/search?q={search}",new=2)
                continue

            if jarvis_quest[0] == "sage" and len(jarvis_quest) > 1:
                words = jarvis_quest[1:]
                sentence = " ".join(words)
                say(sentence)
                continue

            if jarvis_quest[0] in ["öffne", "öffnet", "öffnen", "öffner", "starte", "startet", "starter"] and len(jarvis_quest) > 1:
                app = jarvis_quest[1:]
                app_name = " ".join(app)

                if app_name in ["github"]:
                    webbrowser.get('chrome').open(f"https://github.com",new=2)
                    continue

                if app_name in ["twitch", "switch"]:
                    webbrowser.get('chrome').open(f"https://twitch.tv",new=2)
                    continue

                app_found = False
                for names, exe in known_apps:
                    if app_name in names:
                        app_found = True
                        subprocess.Popen(exe, stderr=subprocess.PIPE)
                        
                        icon = "icons/apps/" + str(ExeUtils.get_exe_name(exe) + ".ico")
                        if not os.path.exists(icon):
                            ExeUtils.extract_icon(exe)

                        notify(f"Started {app_name}", f"The App {app_name} was started!", app_icon=icon)

                        Logger.warning(f"Started {app_name} ({exe})!")
                        continue

                if not app_found:
                    say("Ich konnte die App nicht finden")
                    Logger.warning(f"App not found {app_name}")
                continue

            if jarvis_quest[0] == "frage" and len(jarvis_quest) > 1:
                if jarvis_quest[1] in chatbot_names:
                    start_chatgbt(jarvis_quest[1:])
                    continue

            notify("No Response found!", f"No response for {" ".join(jarvis_quest)} found!", app_icon="icons/no.ico")

            