# File: quotes.py
import requests
import random

def get_random_quote():
    """Get an inspiring quote from API"""
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            return f"💭 Quote: \"{data['content']}\" - {data['author']}"
        else:
            return get_offline_quote()
    except:
        return get_offline_quote()

def get_offline_quote():
    """Backup quotes when API fails"""
    quotes = [
        "Be yourself; everyone else is already taken. - Oscar Wilde",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Life is what happens to you while you're busy making other plans. - John Lennon"
    ]
    return f"💭 Quote: {random.choice(quotes)}"

def get_programming_quote():
    """Get coding-specific quotes"""
    prog_quotes = [
        "Code is like humor. When you have to explain it, it's bad. - Cory House",
        "Programs must be written for people to read. - Harold Abelson",
        "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler"
    ]
    return f"💻 Code Quote: {random.choice(prog_quotes)}"