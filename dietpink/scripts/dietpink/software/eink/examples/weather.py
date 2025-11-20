"""
Weather display for dietpink
(Simulated - can be integrated with real API in the future)
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import time
import random

def get_weather_data():
    """Simulate weather data (replace with real API)"""
    conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']
    return {
        'condition': random.choice(conditions),
        'temp': random.randint(15, 28),
        'humidity': random.randint(40, 80),
        'wind': random.randint(5, 25)
    }

def draw_weather_icon(display, condition, x, y):
    """Draw weather icon (simple symbol)"""
    if condition == 'Sunny':
        # Sun
        display.circle(x, y, 15, fill=display.BLACK)
        # Rays
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            x1 = x + int(20 * math.cos(rad))
            y1 = y + int(20 * math.sin(rad))
            x2 = x + int(28 * math.cos(rad))
            y2 = y + int(28 * math.sin(rad))
            display.line(x1, y1, x2, y2, width=2)
    
    elif condition == 'Cloudy':
        # Cloud
        display.circle(x-8, y, 8, fill=display.BLACK)
        display.circle(x, y-5, 10, fill=display.BLACK)
        display.circle(x+8, y, 8, fill=display.BLACK)
    
    elif condition == 'Rainy':
        # Cloud
        display.circle(x-8, y-5, 8, outline=display.BLACK, width=2)
        display.circle(x, y-10, 10, outline=display.BLACK, width=2)
        display.circle(x+8, y-5, 8, outline=display.BLACK, width=2)
        # Drops
        for i in range(3):
            display.line(x-8+i*8, y+5, x-8+i*8, y+12, width=2)
    
    else:  # Partly Cloudy
        # Small sun
        display.circle(x-10, y-10, 8, outline=display.BLACK, width=2)
        # Cloud
        display.circle(x, y+5, 8, fill=display.BLACK)
        display.circle(x+8, y, 10, fill=display.BLACK)

def main():
    print("🌤️  Weather display...")
    
    with DietpinkDisplay() as display:
        weather = get_weather_data()
        
        display.clear()
        
        # Header
        display.rectangle(0, 0, 250, 28, fill=display.BLACK)
        display.text("Weather", 10, 6, size='medium', color=display.WHITE)
        display.text(time.strftime('%H:%M'), 200, 6, size='medium', 
                   color=display.WHITE)
        
        # Weather icon
        draw_weather_icon(display, weather['condition'], 50, 60)
        
        # Large temperature
        display.text(f"{weather['temp']}°C", 100, 45, size='huge')
        
        # Condition
        display.text(weather['condition'], 125, 85, size='medium', align='center')
        
        # Details
        y = 100
        display.text(f"💧 {weather['humidity']}%", 10, y, size='small')
        display.text(f"💨 {weather['wind']}km/h", 130, y, size='small')
        
        display.refresh()
        print("✅ Weather displayed")
        time.sleep(5)

if __name__ == "__main__":
    main()