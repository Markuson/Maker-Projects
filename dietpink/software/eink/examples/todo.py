"""
Simple To-Do list for dietpink
Shows tasks with checkboxes
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import time

# Task list (True = completed, False = pending)
TASKS = [
    (True, "Install DietPi"),
    (True, "Setup e-ink HAT"),
    (True, "Create wrapper"),
    (False, "Add weather API"),
    (False, "Setup auto-start"),
]

def draw_checkbox(display, x, y, checked, size=10):
    """Draw checkbox"""
    # Box
    display.rectangle(x, y, size, size, outline=display.BLACK, width_line=2)
    
    # Check if marked
    if checked:
        display.line(x+2, y+5, x+4, y+8, width=2)
        display.line(x+4, y+8, x+8, y+2, width=2)

def main():
    print("📝 To-Do list...")
    
    with DietpinkDisplay() as display:
        display.clear()
        
        # Header
        display.rectangle(0, 0, 250, 28, fill=display.BLACK)
        display.text("To-Do List", 10, 6, size='medium', color=display.WHITE)
        completed = sum(1 for done, _ in TASKS if done)
        display.text(f"{completed}/{len(TASKS)}", 200, 6, size='medium', 
                   color=display.WHITE)
        
        # Tasks
        y = 35
        for i, (done, task) in enumerate(TASKS):
            if y > 100:  # Don't show more if it doesn't fit
                break
            
            # Checkbox
            draw_checkbox(display, 10, y, done)
            
            # Task text
            display.text(task, 28, y-2, size='small')
            
            y += 15
        
        # Footer
        display.line(10, 108, 240, 108)
        display.text("dietpink", 125, 112, size='tiny', align='center')
        
        display.refresh()
        print("✅ To-Do displayed")
        time.sleep(5)

if __name__ == "__main__":
    main()