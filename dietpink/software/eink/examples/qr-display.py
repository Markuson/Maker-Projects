#!/usr/bin/env python3
"""
Generate and display QR code on display
Useful for sharing URLs, WiFi, etc.
"""

import sys
sys.path.append('/root/projects/dietpink/software/eink')

from dietpink_display import DietpinkDisplay
import qrcode
from PIL import Image
import time

def generate_qr(data, size=100):
    """
    Generate QR code
    
    Args:
        data: Data to encode (URL, text, etc.)
        size: Size in pixels
    
    Returns:
        PIL Image of QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))
    
    return img

def main():
    # Get data from arguments or use default
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        # Default: system IP
        import subprocess
        try:
            ip = subprocess.check_output(['hostname', '-I']).decode().strip().split()[0]
            data = f"http://{ip}"
        except:
            data = "https://dietpink.local"
    
    print(f"📱 Generating QR code for: {data}")
    
    with DietpinkDisplay() as display:
        display.clear()
        
        # Header
        display.rectangle(0, 0, 250, 25, fill=display.BLACK)
        display.text("QR Code", 125, 5, size='medium', 
                   color=display.WHITE, align='center')
        
        # Generate QR
        qr_img = generate_qr(data, size=90)
        
        # Convert to 1-bit and display
        qr_img = qr_img.convert('1')
        display.image.paste(qr_img, (80, 30))
        
        # Explanatory text
        # Truncate if too long
        display_text = data if len(data) < 35 else data[:32] + "..."
        display.text(display_text, 125, 123, size='tiny', align='center')
        
        display.refresh()
        print("✅ QR code displayed")
        print("   Scan with your phone!")
        time.sleep(10)

if __name__ == "__main__":
    main()