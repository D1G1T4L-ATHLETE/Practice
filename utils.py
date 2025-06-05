# File: utils.py
from datetime import datetime
import random
import time
import requests

def get_fun_fact():
    """Get a random fun fact"""
    facts = [
        "Honey never spoils! Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old.",
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have three hearts and blue blood!",
        "Bananas are berries, but strawberries aren't.",
        "Wombat poop is cube-shaped."
    ]
    return f"🤔 Fun Fact: {random.choice(facts)}"

def get_current_time():
    """Get formatted current date and time"""
    now = datetime.now()
    return {
        'date': now.strftime('%A, %B %d, %Y'),
        'time': now.strftime('%I:%M %p'),
        'timestamp': now
    }

def loading_animation(message="Loading", dots=3, delay=0.5):
    """Show a loading animation"""
    print(message, end="")
    for i in range(dots):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()

def create_divider(char="=", length=60):
    """Create a visual divider"""
    return char * length

def get_daily_joke():
    """Get a daily joke from an API or fallback"""
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"😂 Joke: {data['setup']} {data['punchline']}"
    except Exception:
        pass
    # Fallback joke
    jokes = [
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "Why do programmers prefer dark mode? Because light attracts bugs."
    ]
    return f"😂 Joke: {random.choice(jokes)}"