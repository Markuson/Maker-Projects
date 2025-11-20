"""
Display a simple message on the display
Useful for calling from bash scripts
Example: python3 message.py "Hello World"
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import time

def show_message(title, message, duration=5):
    """
    Show a message on the display
    
    Args:
        title: Message title
        message: Message text (can have multiple lines with \n)
        duration: Seconds to display
    """
    with DietpinkDisplay() as display:
        display.clear()
        
        # Header
        display.rectangle(0, 0, 250, 28, fill=display.BLACK)
        display.text(title, 125, 6, size='medium', 
                   color=display.WHITE, align='center')
        
        # Message (split into lines if it has \n)
        lines = message.split('\n')
        y = 40
        spacing = 20
        
        for line in lines:
            display.text(line, 125, y, size='medium', align='center')
            y += spacing
        
        # Footer with time
        display.line(10, 108, 240, 108)
        display.text(time.strftime('%H:%M:%S'), 125, 112, 
                   size='tiny', align='center')
        
        display.refresh()
        time.sleep(duration)

def main():
    # Get arguments
    if len(sys.argv) < 2:
        print("Usage: python3 message.py <message> [title] [duration]")
        print("Example: python3 message.py 'Hello World' 'Info' 5")
        sys.exit(1)
    
    message = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "dietpink"
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    show_message(title, message, duration)
    print(f"✅ Message displayed for {duration} seconds")

if __name__ == "__main__":
    main()