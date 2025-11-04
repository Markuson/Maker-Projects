"""
Rellotge digital simple per dietpink
Actualitza cada segon amb partial refresh
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import time

def main():
    print("🕐 Iniciant rellotge dietpink...")
    print("   Prem Ctrl+C per aturar")
    
    with DietpinkDisplay() as display:
        try:
            while True:
                # Clear canvas
                display.clear()
                
                # Header amb data
                display.rectangle(0, 0, 250, 28, fill=display.BLACK)
                date_str = time.strftime('%A, %d %B %Y')
                display.text(date_str, 125, 6, size='small', 
                           color=display.WHITE, align='center')
                
                # Hora gran al centre
                time_str = time.strftime('%H:%M')
                display.text(time_str, 125, 50, size='huge', align='center')
                
                # Segons petits sota
                seconds_str = time.strftime(':%S')
                display.text(seconds_str, 125, 90, size='medium', align='center')
                
                # Footer
                display.line(10, 108, 240, 108)
                display.text("dietpink clock", 125, 112, size='tiny', align='center')
                
                # Refresh amb partial (més ràpid, menys flickering)
                display.refresh(partial=True)
                
                # Esperar 1 segon
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️  Rellotge aturat")
            display.clear()
            display.text("Clock stopped", 125, 60, size='medium', align='center')
            display.refresh()

if __name__ == "__main__":
    main()
