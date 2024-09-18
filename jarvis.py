import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose default voice


def speak(audio):
    """Converts text to speech."""
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """Greets the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")


def takeCommand():
    """Listens to the microphone and returns the user's spoken input as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Adjust the threshold if needed
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand the audio, please say that again.")
        return "None"
    except sr.RequestError:
        print("Request error from Google Speech Recognition service.")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"
    return query


def sendEmail(to, content):
    """Sends an email using the provided credentials and content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Login using your credentials (use environment variables for security in production)
        server.login('youremail@gmail.com', 'your-password')  # Replace with your credentials
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I am not able to send this email")


if __name__ == "__main__":
    wishMe()  # Greets the user
    while True:
        query = takeCommand().lower()

        # Execute tasks based on the query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"Disambiguation error: {e.options}")
                speak("There are multiple results, please be more specific.")
            except wikipedia.exceptions.PageError:
                print("Page not found.")
                speak("Sorry, I couldn't find any relevant information.")
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'  # Update this to the correct path
            try:
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))
            except FileNotFoundError:
                speak("Music directory not found.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  # Update this to your correct path
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harryyourEmail@gmail.com"  # Update the recipient email
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry my friend Harry, I am not able to send this email.")
