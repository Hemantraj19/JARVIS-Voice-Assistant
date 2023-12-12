import pyttsx3
import datetime
import speech_recognition as sr
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.webdriver.common.action_chains import ActionChains
import wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient
import clipboard
import pyautogui
import pyjokes
import string
import random
import psutil
from nltk.tokenize import word_tokenize
from selenium.common.exceptions import TimeoutException
import socketio

engine = pyttsx3.init()
sio = socketio.Client()

@sio.on('status_update')
def handle_status_update(data):
    print(f"Received status update: {data['status']}")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def change_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
def change_rate(rate):
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print(rate)                        #printing current voice rate
    engine.setProperty('rate', rate) 

def get_time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is "+Time)

def get_date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("Today's date is")
    speak(day)
    speak(month)
    speak(year)

def greeting():
    hour = datetime.datetime.now().hour
    greetings = {
        range(6, 12): "Good Morning",
        range(12, 18): "Good Afternoon",
        range(18, 24): "Good Evening",
        range(0, 6): "Good Night"
    }
    
    greet = greetings.get(next((key for key in greetings if hour in key), ""), "Default Greeting")
    speak(greet)

def bootup():
    greeting()
    speak("Welcome back sir!")
    speak("Jarvis at your service. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        sio.emit('status_update', {'status': 'Listening...'})
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        sio.emit('status_update', {'status': 'Recognizing...'})
        query = r.recognize_google(audio, language='en-IN')
        print(query)
    except Exception as e:
        print(e)
        print("Please say that again...")
        return "None"
    return query


def send_whatsapp_message():

    speak("Whom do you want to send the message to?")
    name = take_command()
    speak("What is the message?")
    message = take_command()
    name = name.lower()
    
    if 'none' in name or 'none' in message:
        speak("Message not sent. Please try again.")
        return
    
    speak("Sending message to"+name)

    # Install the appropriate version of ChromeDriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\environments\\selenium")
    # options.add_argument("--log-path=C:\\environments\\selenium\\chromedriver.log")
    driver = webdriver.Chrome(options=options)

    try:

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com/")

        # Wait until the search box is clickable
        max_timeout = 60  # maximum time to wait in seconds
        current_timeout = 0

        while current_timeout < max_timeout:
            try:
                element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='g0rxnol2 ln8gz9je lexical-rich-text-input']//div[@contenteditable='true'][@role='textbox']")))
                element.click()
                break  # Break out of the loop if element is found and clicked
            except TimeoutException:
                current_timeout += 1
                print(f"Timeout exception at {current_timeout} seconds.")

        # Locate the search box and type the contact name
        search_box = driver.find_element(By.XPATH, "//div[@class='g0rxnol2 ln8gz9je lexical-rich-text-input']//div[@contenteditable='true'][@role='textbox']")
        search_box.send_keys(name)

        # Wait until the contact is clickable in the search results
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]")))

        # Select the contact from the search results
        contact_selector = driver.find_element(By.XPATH, f"//span[contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{name}')]")
        contact_selector.click()

        # Wait until the message box is clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_3Uu1_']//div[@class='g0rxnol2 ln8gz9je lexical-rich-text-input']//div[@contenteditable='true'][@role='textbox']")))

        # Type the message in the input box
        message_box = driver.find_element(By.XPATH, "//div[@class='_3Uu1_']//div[@class='g0rxnol2 ln8gz9je lexical-rich-text-input']//div[@contenteditable='true'][@role='textbox']")
        message_box.send_keys(message)

        # Press Enter to send the message
        action = ActionChains(driver)
        action.send_keys(Keys.RETURN)
        action.perform()

        time.sleep(5)

        print("Message sent successfully")
        

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Close the browser window
        driver.quit()
        speak("Message sent successfully")
        
        
def search_wikipedia():
    speak("What do you want to search for?")
    query = take_command()
    
    try:
        speak("Searching Wikipedia...")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found for {query}. Please specify your search.")
    except wikipedia.exceptions.PageError as e:
        speak(f"No results found for {query}. Please try a different search term.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia. Please try again later.")
        print(f"Error: {e}")
        

def search_google():
    speak("What do you want to search for?")
    search_term = take_command()
    search_term = search_term.lower()
    search_term = search_term.replace(' ', '+')
    speak("Searching Google...")
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={search_term}")
    speak("If you want to close the browser, say close")
    while True:
        query = take_command()
        if 'close' in query:
            driver.quit()
            break
        else:
            continue
        
def play_video_on_youtube():
    speak("What do you want to play?")
    search_term = take_command()
    speak("Playing"+ search_term +"on YouTube")
    pywhatkit.playonyt(search_term)
    
def weather_update():
    api_key = '72a1fafd1bf851c78a4c08951be15aa2'
    url = f'https://api.openweathermap.org/data/2.5/weather?q=ranchi&appid={api_key}'

    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an HTTPError for bad responses
        data = res.json()

        if 'weather' in data:
            weather = data['weather'][0]['main']
            temp = data['main']['temp']
            temp_celsius = round((temp - 273.15), 2)
            speak(f"The weather in Ranchi is {weather} and the temperature is {temp_celsius} degrees Celsius.")
        else:
            speak("Unable to fetch weather information.")
    except requests.exceptions.RequestException as e:
        speak(f"An error occurred during the weather update: {str(e)}")
        
def get_news_update():
    newsapi = NewsApiClient(api_key='56c2b21ee3d44b29bf78425f73610470')
    top_headlines = newsapi.get_top_headlines(language='en', country='in',page_size=5)
    articles = top_headlines['articles']
    change_rate(150)
    for article in articles:
        speak(article['title'])
        # speak("Moving on to the next news headline.")
        time.sleep(0.5)
    speak("That's all for now.")
    change_rate(230)
    
def copy_to_speech():
    text = clipboard.paste()
    speak(text)
    
    
def open_application_by_search():
    
    speak("What is the name of the application?")
    app_name = take_command()
    app_name = app_name.lower()
    try:
        # Open the Windows search bar using the Windows key
        pyautogui.press('win')

        # Type the application name in the search bar
        pyautogui.write(app_name)
        time.sleep(1)  # Wait for search results to appear

        # Press Enter to open the first result
        pyautogui.press('enter')

        print(f"Searching for and opening {app_name}")
    except Exception as e:
        print(f"Error opening application: {str(e)}")
        
        
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    
def take_screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\\Hemant\\Pictures\\Screenshots\\{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
    speak("Screenshot taken successfully")
    img.show()
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'w')
    

def remember():
    speak("What do you want me to remember?")
    data = take_command()
    speak("You asked me to remember "+data)
    remember = open('data.txt', 'w')
    remember.write(data)
    remember.close()
    
def remind():
    remember = open('data.txt', 'r')
    speak("You asked me to remember "+remember.read())
    remember.close()
    
def generate_password():
    password = ""
    speak("Generating password...")
    for _ in range(10):
        password += random.choice(string.ascii_letters + string.digits + string.punctuation)
    print(password)
    speak("Your password is "+password)
    
def cpu_usage():
    usage = str(psutil.cpu_percent())
    speak("CPU is at "+usage+" percent")
    
def battery_status():
    battery = psutil.sensors_battery()
    speak("Battery is at "+str(battery.percent)+" percent")
    
def turn_off():
    speak("Do you want to turn off the system?")
    query = take_command()
    if 'yes' in query:
        speak("Turning off the system, goodbye sir")
        os.system("shutdown /s /t 1")
    else:
        speak("Aborting shutdown")
        
def restart():
    speak("Restarting the system")
    os.system("shutdown /r /t 1")
        
def go_offline():
    speak("Goodbye sir!")
    quit()
        

commands = {
    'time': get_time,
    'date': get_date,
    'whatsapp': send_whatsapp_message,
    'wikipedia': search_wikipedia,
    'google': search_google,
    'youtube': play_video_on_youtube,
    'song': play_video_on_youtube,
    'weather': weather_update,
    'news': get_news_update,
    'read': copy_to_speech,
    'open': open_application_by_search,
    'joke': tell_joke,
    'screenshot': take_screenshot,
    'remember': remember,
    'remind': remind,
    'password': generate_password,
    'cpu': cpu_usage,
    'battery': battery_status,
    'shutdown': turn_off,
    'turn': turn_off,
    'restart': restart,
    'offline': go_offline
}

def process_query(query):
    # Process the query using the commands dictionary
    for keyword, function in commands.items():
        if keyword in query:
            function()
  
    

if __name__ == "__main__":
    sio.connect('http://127.0.0.1:5000/')
    change_rate(230)
    change_voice()
    bootup()
    wakeword = "jarvis"
    while True:
        query = take_command().lower()
        query = word_tokenize(query)
        print(query)

        if wakeword in query:
            process_query(query)