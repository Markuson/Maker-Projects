"""
Simple digital clock for dietpink
Updates every second with partial refresh
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import time

def main():
    print("🕐 Starting dietpink clock...")
    print("   Press Ctrl+C to stop")
    
    with DietpinkDisplay() as display:
        try:
            while True:
                # Clear canvas
                display.clear()
                
                # Header with date
                display.rectangle(0, 0, 250, 28, fill=display.BLACK)
                date_str = time.strftime('%A, %d %B %Y')
                display.text(date_str, 125, 6, size='small', 
                           color=display.WHITE, align='center')
                
                # Large time in center
                time_str = time.strftime('%H:%M')
                display.text(time_str, 125, 50, size='huge', align='center')
                
                # Small seconds below
                seconds_str = time.strftime(':%S')
                display.text(seconds_str, 125, 90, size='medium', align='center')
                
                # Footer
                display.line(10, 108, 240, 108)
                display.text("dietpink clock", 125, 112, size='tiny', align='center')
                
                # Refresh with partial (faster, less flickering)
                display.refresh(partial=True)
                
                # Wait 1 second
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️  Clock stopped")
            display.clear()
            display.text("Clock stopped", 125, 60, size='medium', align='center')
            display.refresh()

if __name__ == "__main__":
    main()
