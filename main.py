import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

#pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_API_KEY"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the audio
    pygame.mixer.music.play()

    # Keep the program running until the music ends
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Prevents the script from closing immediately

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(
    api_key = "OPENAI_API_KEY",
    )
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", "content": "You are a virtual assistant named jarvis, skilled in general tasks like alexa and google cloud. Give short responses"
        },
        {
            "role": "user",
            "content": command
        }
    ]
    )

    return completion.choices[0].message.content
    



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            #Print the headlines
            for article in articles:
                print(article['title'])


    else:
        #Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)
            
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
    #Listen for the wake word "Jarvis"
    #Obtaining audio
        r = sr.Recognizer()
      
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
        

                    processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))
