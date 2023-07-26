import speech_recognition as sr # voice recognition
import pyttsx3 # voice 
import subprocess # open apps
import requests # weather
import datetime # Date and time
import bluetooth # bluetooth

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except sr.RequestError as e:
        print("Request Error:", str(e))

    return ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

# weather
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] == "404":
        return "City not found."
    else:
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {description}. Temperature: {temperature}°C. Humidity: {humidity}%."
    
# Time    
def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {current_time}")

# Date
def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d")
    speak(f"Today's date is {current_date}")

# bluetooth
def connect_to_bluetooth(device_name):
    nearby_devices = bluetooth.discover_devices(lookup_names=True)

    for addr, name in nearby_devices:
        if device_name.lower() in name.lower():
            try:
                bluetooth.connect(addr)
                return f"Connected to {name}."
            except Exception as e:
                return f"Error connecting to {name}: {e}"

    return "Bluetooth device not found."

def assistant():
    weather_api_key = "ac83d86e4d234fc98bccbec87daefd4f"
    
    while True:
        command = listen().lower()

        if "hello" in command:
            speak("Hey Aiman, what's up?")

        elif "what's your name" in command:
            speak("I am Tinkus, your virtual assistant.")

        elif "how old are you" in command:
            speak("I was born in July 24th, 2023.")
        
        elif "how are you" in command:
            speak("I am doing great. Thank you for asking.")
        
        elif "thank you" in command:
            speak("No problem!")    

        # open apps
        elif "open chrome" in command:
            speak("Opening Google Chrome...")
            try:
                subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe"]) 
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I couldn't open Google Chrome.")

        # weather
        elif "what's the weather" in command:
            city = input("Which city's weather would you like to know? ")
            result = get_weather(city, weather_api_key)
            speak(result)

        # Time
        elif "tell time" in command:
            tell_time()

        # Date
        elif "tell date" in command:
            tell_date()

        # bluetooth
        elif "connect bluetooth" in command:
            device_name = input("Which Bluetooth device would you like to connect to? ")
            result = connect_to_bluetooth(device_name)
            speak(result)

        # Stop
        elif "stop" in command:
            speak("Goodbye Aiman!")
            break

        # Add more commands and responses as needed

        else:
            speak("Sorry, I don't understand.")

# Run the assistant
assistant()