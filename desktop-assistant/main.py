import speech_recognition as sr
import os
import webbrowser
import requests
import random
from datetime import datetime
import shlex
import wikipedia
# Use a pipeline as a high-level helper
from transformers import pipeline

chatbot = pipeline("text-generation", model="openai-community/gpt2")

def say(text):
    os.system(f"say {shlex.quote(text)}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query
        except Exception:
            return "Sorry, I didn't catch that."

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")


def get_weather(city):
    api_key = '6494dab039285b0ac8b389c1730d866c'  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data.get("cod") != 200:  # Check if the response is successful
        return "City not found. Please check the name."

    main = data["main"]
    temperature = main["temp"]
    weather_description = data["weather"][0]["description"]
    return f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}."


def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the math book look sad? Because it had too many problems."
    ]
    return random.choice(jokes)



def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"This query may refer to multiple topics: {e.options}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find that on Wikipedia."
    except Exception:
        return "An error occurred while searching Wikipedia."



def chat_with_model(query):
    # Generate a response using the model with truncation and padding settings
    response = chatbot(
        query,
        max_length=50,
        num_return_sequences=1,
        truncation=True,
        pad_token_id=50256
    )
    return response[0]['generated_text'].strip()




if __name__ == '_main_':
    print('Starting...')
    say("Hello, I am your A I friend.how can i help you")

    while True:
        print("Listening...")
        query = takeCommand()
        if 'stop' in query.lower():
            print("Goodbye!")
            say("Goodbye!")
            break


        if 'weather' in query.lower():
            city = query.split("in")[-1].strip()  # Extract city from the query3
            weather_info = get_weather("Ludhiana, IN")
            print(weather_info)
            say(weather_info)

        elif 'joke' in query.lower():
            joke = tell_joke()
            print(joke)
            say(joke)

        elif 'time' in query.lower() or 'date' in query.lower():
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")
            print(f"The current time is {current_time} and today's date is {current_date}.")
            say(f"The current time is {current_time} and today's date is {current_date}.")

        elif 'open' in query.lower():
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["wikipedia", "https://www.wikipedia.com"],
                ["google", "https://www.google.com"],
                ["facebook", "https://www.facebook.com"],
                ["twitter", "https://www.twitter.com"],
                ["instagram", "https://www.instagram.com"],
                ["linkedin", "https://www.linkedin.com"],
                ["reddit", "https://www.reddit.com"],
                ["github", "https://www.github.com"],
                ["stackoverflow", "https://www.stackoverflow.com"],
                ["news", "https://news.google.com"],
                ["medium", "https://www.medium.com"],
                ["quora", "https://www.quora.com"],
                ["pinterest", "https://www.pinterest.com"]
            ]
            for site in sites:
                if f"open {site[0]}" in query.lower():
                    say(f"Opening {site[0]} for you.")
                    webbrowser.open(site[1])
                    break



        elif 'search' in query.lower():
            search_query = query.lower().replace("search", "").strip()
            if 'wikipedia' in query.lower():
                result = search_wikipedia(search_query)
                say(result)
            else:
                search_web(search_query)
                say(f"Here are the search results for {search_query}.")
        if "open music" in query:
            musicPath="/Data/Users/gurshangrewal/Music/Music/Media/Music/Unknown Artist/Unknown Album/Shape Of You.mp3"
            os.system(f"open {musicPath}")

        elif 'talk' in query.lower() or 'chat' in query.lower():
            say("What would you like to talk about?")
            chat_query = takeCommand()
            response = chat_with_model(chat_query)
            print(response)
            say(response)
            