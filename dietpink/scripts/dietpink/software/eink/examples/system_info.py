"""
Display system information on dietpink
Temperature, CPU, RAM, Disk
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import subprocess
import time

def get_cpu_temp():
    """Get CPU temperature"""
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        return temp.replace('temp=', '').replace("'C\n", '').strip()
    except:
        return "N/A"

def get_cpu_usage():
    """Get CPU usage % (approximated from load average)"""
    try:
        # Load average for 1 min
        load = subprocess.check_output(['cat', '/proc/loadavg']).decode().split()[0]
        # Pi Zero W has 1 core, so load 1.0 = 100%
        percentage = min(float(load) * 100, 100)
        return f"{percentage:.0f}%"
    except:
        return "N/A"

def get_memory():
    """Get memory used"""
    try:
        mem = subprocess.check_output(['free', '-h']).decode().split('\n')[1].split()
        used = mem[2]
        total = mem[1]
        return f"{used}/{total}"
    except:
        return "N/A"

def get_disk():
    """Get disk space"""
    try:
        disk = subprocess.check_output(['df', '-h', '/']).decode().split('\n')[1].split()
        used = disk[2]
        total = disk[1]
        percent = disk[4]
        return f"{used}/{total} ({percent})"
    except:
        return "N/A"

def get_ip():
    """Get wlan0 IP"""
    try:
        ip = subprocess.check_output(['hostname', '-I']).decode().strip().split()[0]
        return ip
    except:
        return "N/A"

def main():
    print("💻 System info display...")
    
    with DietpinkDisplay() as display:
        display.clear()
        
        # Header
        display.rectangle(0, 0, 250, 28, fill=display.BLACK)
        display.text("System Info", 10, 6, size='medium', color=display.WHITE)
        display.text(time.strftime('%H:%M'), 200, 6, size='medium', 
                   color=display.WHITE)
        
        # System info
        y = 35
        spacing = 15
        
        display.text(f"IP:   {get_ip()}", 10, y, size='small')
        y += spacing
        
        display.text(f"Temp: {get_cpu_temp()}", 10, y, size='small')
        y += spacing
        
        display.text(f"CPU:  {get_cpu_usage()}", 10, y, size='small')
        y += spacing
        
        display.text(f"RAM:  {get_memory()}", 10, y, size='small')
        y += spacing
        
        display.text(f"Disk: {get_disk()}", 10, y, size='small')
        
        # Footer
        display.line(10, 108, 240, 108)
        display.text("dietpink", 125, 112, size='tiny', align='center')
        
        display.refresh()
        
        print("✅ Info displayed")
        print("   Screen will stay for 10 seconds...")
        time.sleep(10)

if __name__ == "__main__":
    main()