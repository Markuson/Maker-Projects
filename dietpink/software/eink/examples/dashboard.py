"""
Complete dashboard for dietpink
Shows time, temperature and statistics with progress bars
Updates automatically every 5 seconds
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import subprocess
import time

def get_stats():
    """Get system statistics"""
    stats = {}
    
    # Temperature
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        stats['temp'] = temp.replace('temp=', '').replace("'C\n", '').strip()
    except:
        stats['temp'] = 'N/A'
    
    # CPU usage (load average)
    try:
        load = subprocess.check_output(['cat', '/proc/loadavg']).decode().split()[0]
        stats['cpu'] = min(int(float(load) * 100), 100)
    except:
        stats['cpu'] = 0
    
    # Memory usage
    try:
        mem = subprocess.check_output(['free']).decode().split('\n')[1].split()
        total = int(mem[1])
        used = int(mem[2])
        stats['mem'] = int((used / total) * 100)
    except:
        stats['mem'] = 0
    
    # Disk usage
    try:
        disk = subprocess.check_output(['df', '/']).decode().split('\n')[1].split()
        stats['disk'] = int(disk[4].replace('%', ''))
    except:
        stats['disk'] = 0
    
    return stats

def main():
    print("📊 dietpink dashboard starting...")
    print("   Updates every 5 seconds")
    print("   Press Ctrl+C to stop")
    
    with DietpinkDisplay() as display:
        iteration = 0
        
        try:
            while True:
                display.clear()
                
                # Black header with title and time
                display.rectangle(0, 0, 250, 28, fill=display.BLACK)
                display.text("dietpink", 10, 6, size='medium', color=display.WHITE)
                display.text(time.strftime('%H:%M:%S'), 190, 6, size='medium', 
                           color=display.WHITE)
                
                # Date and temperature
                y = 35
                display.text(time.strftime('%d/%m/%Y'), 10, y, size='small')
                
                # Get statistics
                stats = get_stats()
                display.text(f"{stats['temp']}°C", 190, y, size='small')
                
                # Separator
                display.line(10, 50, 240, 50)
                
                # Progress bars amb labels
                y = 58
                spacing = 18
                
                # CPU
                display.text("CPU", 10, y, size='tiny')
                display.progress_bar(45, y, 170, 12, stats['cpu'])
                display.text(f"{stats['cpu']}%", 220, y, size='tiny')
                y += spacing
                
                # RAM
                display.text("RAM", 10, y, size='tiny')
                display.progress_bar(45, y, 170, 12, stats['mem'])
                display.text(f"{stats['mem']}%", 220, y, size='tiny')
                y += spacing
                
                # Disk
                display.text("Disk", 10, y, size='tiny')
                display.progress_bar(45, y, 170, 12, stats['disk'])
                display.text(f"{stats['disk']}%", 220, y, size='tiny')
                
                # Footer
                display.line(10, 108, 240, 108)
                display.text(f"Update #{iteration+1}", 125, 112, 
                           size='tiny', align='center')
                
                # Refresh (partial after first iteration)
                if iteration == 0:
                    display.refresh(partial=False)  # First refresh: full
                else:
                    display.refresh(partial=True)   # Subsequent: partial
                
                iteration += 1
                
                # Update every 5 seconds
                time.sleep(5)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Dashboard stopped after {iteration} updates")
            display.clear()
            display.text("Dashboard", 125, 50, size='large', align='center')
            display.text("stopped", 125, 75, size='medium', align='center')
            display.refresh()

if __name__ == "__main__":
    main()