# File: main.py
# Import your custom modules
from data_sources.weather import get_weather, get_forecast
from quotes import get_random_quote, get_programming_quote
from utils import get_fun_fact, get_current_time, loading_animation, create_divider, get_daily_joke

def create_dashboard():
    """Main dashboard function"""
    print(create_divider())
    print("🌟 YOUR DAILY DASHBOARD 🌟")
    print(create_divider())
    
    time_info = get_current_time()
    print(f"📅 Date: {time_info['date']}")
    print(f"⏰ Time: {time_info['time']}")
    print(create_divider("-"))
    
    loading_animation("Loading your personalized info")
    
    # Use functions from different modules
    print(get_weather())
    print()
    print(get_random_quote())
    print()
    print(get_programming_quote())
    print()
    print(get_fun_fact())
    print()
    print(get_daily_joke())  # <-- Show the daily joke
    print()
    
    # Show forecast
    print("📊 5-Hour Forecast:")
    forecasts = get_forecast()
    for forecast in forecasts[:3]:  # Show first 3
        print(f"   {forecast}")
    
    print()
    print(create_divider())
    print("Have a great day! 🚀")
    print(create_divider())

if __name__ == "__main__":
    create_dashboard()