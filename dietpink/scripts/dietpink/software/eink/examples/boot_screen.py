#!/usr/bin/env python3
"""
Boot screen for dietpink
Shows logo, version and boot info
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import subprocess
import time

def get_hostname():
    try:
        return subprocess.check_output(['hostname']).decode().strip()
    except:
        return "dietpink"

def get_ip():
    try:
        return subprocess.check_output(['hostname', '-I']).decode().strip().split()[0]
    except:
        return "No IP"

def main():
    print("🚀 Boot screen...")
    
    with DietpinkDisplay() as display:
        display.clear()
        
        # Large logo text
        display.text("dietpink", 125, 20, size='huge', align='center')
        
        # Version
        display.text("v1.0", 125, 60, size='small', align='center')
        
        # Separator
        display.line(50, 75, 200, 75)
        
        # Info
        y = 82
        display.text(f"Host: {get_hostname()}", 125, y, size='tiny', align='center')
        y += 12
        display.text(f"IP: {get_ip()}", 125, y, size='tiny', align='center')
        y += 12
        display.text(time.strftime('%Y-%m-%d %H:%M'), 125, y, 
                   size='tiny', align='center')
        
        display.refresh()
        print("✅ Boot screen displayed")
        time.sleep(3)

if __name__ == "__main__":
    main()