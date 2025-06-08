import pvporcupine
import pyaudio
import struct
import pyttsx3
import time
import speech_recognition as sr
import os
import requests
import webbrowser
import random
import subprocess
import platform
import psutil
import pyautogui
from datetime import datetime
import glob
import random


access_key = "jb/+kEqCN47QQmG1UC/IEUS8eY/lg1XhOtXgF03UUzhcpg1QxJplcQ=="

porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths=["D:/Project Jarvis/Hey-Jarvis_en_windows_v3_0_0.ppn"]
)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 120)
original_volume = engine.getProperty('volume')
engine.setProperty('volume', 0.0)
engine.say("Priming Jarvis.")
engine.runAndWait()
engine.setProperty('volume', original_volume)
print("Voice engine ready.")

# Simulated calendar (you can expand this)
calendar_events = {
    datetime.now().strftime("%Y-%m-%d"): ["Team meeting at 3 PM", "Submit project report"]
}

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

def get_weather():
    webbrowser.open("https://www.accuweather.com/en/in/ajmer/190208/weather-forecast/190208")
    engine.say("Redirecting you to the weather forecast for Ajmer.")
    engine.runAndWait()

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the computer go to the doctor? It had a virus!"
    ]
    engine.say(random.choice(jokes))
    engine.runAndWait()

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    engine.say(f"Here are the results for {query}")
    engine.runAndWait()

def play_music():
    music_folder = r"D:\Audio"
    songs = os.listdir(music_folder)
    song = random.choice(songs)
    song_path = os.path.join(music_folder, song)
    os.system(f'start wmplayer "{song_path}"')
    engine.say(f"Playing {song}")
    engine.runAndWait()

def roll_dice():
    dice = random.randint(1, 6)
    engine.say(f"You rolled a {dice}.")
    engine.runAndWait()

def toss_coin():
    coin = random.choice(["heads", "tails"])
    engine.say(f"The coin landed on {coin}.")
    engine.runAndWait()


def youtube_search(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    engine.say(f"Searching YouTube for {query}")
    engine.runAndWait()

def open_application(app_name):
    if "notepad" in app_name:
        os.system("notepad")
        engine.say("Opening Notepad.")
        engine.runAndWait()
    elif "calculator" in app_name:
        os.system("start calc")
        engine.say("Opening Calculator.")
        engine.runAndWait()
    else:
        engine.say(f"Sorry, I cannot open {app_name}.")
        engine.runAndWait()

def get_system_info():
    uname = platform.uname()
    battery = psutil.sensors_battery()
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    info = (
        f"System: {uname.system} {uname.release}, "
        f"Machine: {uname.machine}, Processor: {uname.processor}. "
        f"Battery: {battery.percent}% {'plugged in' if battery.power_plugged else 'on battery'}. "
        f"RAM: {ram.percent}% used, CPU Usage: {cpu}%."
    )
    engine.say(info)
    engine.runAndWait()

def battery_status():
    battery = psutil.sensors_battery()
    plugged = "plugged in" if battery.power_plugged else "not plugged in"
    engine.say(f"Battery is at {battery.percent} percent and is {plugged}.")
    engine.runAndWait()

def internet_status():
    try:
        requests.get("https://www.google.com", timeout=3)
        engine.say("You are connected to the internet.")
    except requests.ConnectionError:
        engine.say("You are not connected to the internet.")
    engine.runAndWait()

def take_screenshot():
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(os.getcwd(), filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    engine.say(f"Screenshot saved as {filename}.")
    engine.runAndWait()

def shutdown():
    engine.say("Shutting down your system.")
    engine.runAndWait()
    os.system("shutdown /s /t 1")

def restart():
    engine.say("Restarting your system.")
    engine.runAndWait()
    os.system("shutdown /r /t 1")

def calendar_today():
    today = datetime.now().strftime("%Y-%m-%d")
    if today in calendar_events:
        events = "; ".join(calendar_events[today])
        engine.say(f"You have the following events today: {events}")
    else:
        engine.say("You have no events today.")
    engine.runAndWait()

def search_file(file_name, search_path="C:\\"):
    engine.say(f"Searching for {file_name}. This may take a while.")
    engine.runAndWait()
    pattern = os.path.join(search_path, '**', f'*{file_name}*')
    matches = glob.glob(pattern, recursive=True)
    if matches:
        engine.say(f"Found {len(matches)} file(s). Opening the first one.")
        os.startfile(matches[0])
    else:
        engine.say("No files found with that name.")
    engine.runAndWait()

def execute_command(command):
    if "open" in command and "notepad" in command:
        os.system("notepad")
        engine.say("Opening Notepad.")
        engine.runAndWait()
    elif "hello" in command:
        engine.say("Hello Akshit sir, Jarvis in your active service, How may I help you?")
        engine.runAndWait()
    elif "time" in command:
        current_time = time.strftime("%H:%M:%S")
        engine.say(f"The current time is {current_time}")
        engine.runAndWait()
    elif "date" in command:
        current_date = datetime.now().strftime("%B %d, %Y")
        engine.say(f"Today's date is {current_date}")
        engine.runAndWait()
    elif "calendar" in command:
        calendar_today()
    elif "youtube" in command:
        query = command.replace("youtube", "").strip()
        youtube_search(query)
    elif "file" in command and "search" in command:
        file_name = command.replace("file search", "").strip()
        search_file(file_name)
    elif "open" in command and "calculator" in command:
        os.system("calc")
        engine.say("Opening Calculator.")
        engine.runAndWait()
    elif "play" in command and "music" in command:
        play_music()
    elif "weather" in command:
        get_weather()
    elif "joke" in command:
        tell_joke()
    elif "search" in command:
        query = command.replace("search", "").strip()
        search_web(query)
    elif "system info" in command or "specifications" in command:
        get_system_info()
    elif "battery" in command:
        battery_status()
    elif "internet" in command:
        internet_status()
    elif "take" in command and "screenshot" in command:
        take_screenshot()
    elif "dice" in command and "roll" in command:
        roll_dice()
    elif "toss" in command and "coin" in command:
        toss_coin()
    elif "shutdown" in command:
        shutdown()
        return True
    elif "restart" in command:
        restart()
        return True
    elif "stop listening" in command:
        engine.say("..aahh!.. Okay sir, I think I should sleep now.")
        engine.runAndWait()
        return True
    else:
        engine.say("Sorry, I didn't understand that command.")
        engine.runAndWait()
    return False

print("Listening for wake word...")

try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        audio_data = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(audio_data)
        if keyword_index >= 0:
            print("Wake word detected!")
            engine.say("..aa!.. Hello Akshit sir, Jarvis in your active service, How may I help you?")
            engine.runAndWait()
            while True:
                command = listen_for_commands()
                if command:
                    should_stop = execute_command(command)
                    if should_stop:
                        break
except KeyboardInterrupt:
    print("Stopping...")

finally:
    if porcupine is not None:
        porcupine.delete()
    if stream is not None:
        stream.close()
    if pa is not None:
        pa.terminate()
