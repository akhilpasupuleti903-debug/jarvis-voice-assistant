"""
Jarvis - A Beginner-Friendly Desktop Voice Assistant
This application listens to voice commands and responds with text and speech.
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pyjokes
import sys

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Optional: Adjust speech rate (words per minute)
engine.setProperty('rate', 150)


def speak(text):
    """
    Convert text to speech and play it.
    
    Args:
        text (str): The text to be spoken aloud.
    """
    print(f"Jarvis: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error during speech synthesis: {e}")


def listen():
    """
    Listen to microphone input and convert speech to text.
    
    Returns:
        str: The recognized text from the user, or None if recognition fails.
    """
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise (better accuracy)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
        
        # Try to recognize speech using Google's speech recognition API
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower()
    
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        speak(f"I couldn't connect to the speech recognition service. Please check your internet connection.")
        print(f"Error: {e}")
        return None
    except sr.MicrophoneError:
        speak("I couldn't access your microphone. Please check if it's connected and working properly.")
        print("Error: Microphone not found or not working.")
        return None
    except Exception as e:
        speak("An unexpected error occurred while listening.")
        print(f"Unexpected error: {e}")
        return None


def open_google():
    """Open Google in the default web browser."""
    try:
        speak("Opening Google for you.")
        webbrowser.open("https://www.google.com")
    except Exception as e:
        speak("I couldn't open Google. Please check your internet connection.")
        print(f"Error: {e}")


def open_youtube():
    """Open YouTube in the default web browser."""
    try:
        speak("Opening YouTube for you.")
        webbrowser.open("https://www.youtube.com")
    except Exception as e:
        speak("I couldn't open YouTube. Please check your internet connection.")
        print(f"Error: {e}")


def open_github():
    """Open GitHub in the default web browser."""
    try:
        speak("Opening GitHub for you.")
        webbrowser.open("https://www.github.com")
    except Exception as e:
        speak("I couldn't open GitHub. Please check your internet connection.")
        print(f"Error: {e}")


def search_google(query):
    """
    Search Google for the given query.
    
    Args:
        query (str): The search query.
    """
    try:
        speak(f"Searching Google for {query}")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
    except Exception as e:
        speak("I couldn't perform the search. Please check your internet connection.")
        print(f"Error: {e}")


def search_youtube(query):
    """
    Search YouTube for the given query.
    
    Args:
        query (str): The search query.
    """
    try:
        speak(f"Searching YouTube for {query}")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
    except Exception as e:
        speak("I couldn't search YouTube. Please check your internet connection.")
        print(f"Error: {e}")


def tell_time():
    """Tell the current time."""
    try:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    except Exception as e:
        speak("I couldn't get the current time.")
        print(f"Error: {e}")


def tell_date():
    """Tell the current date."""
    try:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")
    except Exception as e:
        speak("I couldn't get the current date.")
        print(f"Error: {e}")


def tell_joke():
    """Tell a random joke."""
    try:
        joke = pyjokes.get_joke()
        speak(joke)
    except Exception as e:
        speak("I couldn't retrieve a joke right now.")
        print(f"Error: {e}")


def show_help():
    """Display available commands."""
    help_text = """
    ===== JARVIS - Available Commands =====
    1. "open google" - Opens Google
    2. "open youtube" - Opens YouTube
    3. "open github" - Opens GitHub
    4. "search google [query]" - Searches Google for your query
    5. "search youtube [query]" - Searches YouTube for your query
    6. "what time is it" or "tell time" - Tells the current time
    7. "what is today" or "tell date" - Tells the current date
    8. "tell me a joke" - Tells a random joke
    9. "goodbye" or "exit" - Exits the application
    10. "help" - Shows this message
    
    You can also say "list commands" to see this again.
    =======================================
    """
    print(help_text)
    speak("Here are the available commands. Check the terminal for details.")


def process_command(command):
    """
    Process the recognized command and execute the appropriate action.
    
    Args:
        command (str): The recognized command from the user.
    
    Returns:
        bool: True if the application should continue, False if it should exit.
    """
    if command is None:
        return True
    
    # Open websites
    if "open google" in command:
        open_google()
    elif "open youtube" in command:
        open_youtube()
    elif "open github" in command:
        open_github()
    
    # Search functionality
    elif "search google" in command:
        query = command.replace("search google", "").strip()
        if query:
            search_google(query)
        else:
            speak("What would you like me to search for on Google?")
    
    elif "search youtube" in command:
        query = command.replace("search youtube", "").strip()
        if query:
            search_youtube(query)
        else:
            speak("What would you like me to search for on YouTube?")
    
    # Time and date
    elif "what time" in command or "tell time" in command:
        tell_time()
    elif "what is today" in command or "tell date" in command:
        tell_date()
    
    # Jokes
    elif "tell me a joke" in command or "tell a joke" in command:
        tell_joke()
    
    # Help and exit
    elif "help" in command or "list commands" in command:
        show_help()
    elif "goodbye" in command or "exit" in command:
        speak("Goodbye! Have a great day!")
        print("Exiting Jarvis. Bye!")
        return False
    
    # Unknown command
    else:
        speak("Sorry, I didn't understand that command. Would you like to hear the available commands?")
        print("Type 'help' or say 'list commands' to see what I can do.")
    
    return True


def main():
    """
    Main function to run the Jarvis voice assistant.
    Continuously listens for commands until the user exits.
    """
    print("=" * 50)
    print("Welcome to JARVIS - Your Voice Assistant!")
    print("=" * 50)
    speak("Welcome to Jarvis. Say hello, or ask for help to get started.")
    print("\nTip: Say 'help' or 'list commands' to see what I can do.\n")
    
    while True:
        command = listen()
        should_continue = process_command(command)
        
        if not should_continue:
            break
        
        print()  # Add spacing between commands


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting Jarvis.")
        speak("Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        speak("An error occurred. Exiting.")
        sys.exit(1)
