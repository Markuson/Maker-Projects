# 🎨 dietpink

An e-ink dashboard for Raspberry Pi Zero W featuring a WaveShare 2.13" V4 display. A low-power, always-on information display perfect for desks, shelves, or anywhere you want glanceable information without the distraction of a backlit screen.

## 📋 Table of Contents

- [Overview](#overview)
- [Hardware Specifications](#hardware-specifications)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Development Workflow](#development-workflow)
- [API Reference](#api-reference)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

dietpink is a Python-based e-ink display framework that makes it easy to create beautiful, low-power displays for your Raspberry Pi. It includes a custom wrapper around the WaveShare driver that simplifies common operations like drawing text, shapes, progress bars, and updating the display.

**Why e-ink?**
- Ultra-low power consumption (only uses power when updating)
- Excellent readability in bright light
- No eye strain from backlight
- Retains image when powered off
- Perfect for 24/7 information displays

## 🛠️ Hardware Specifications

| Component | Details |
|-----------|---------|
| **Board** | Raspberry Pi Zero W |
| **Display** | WaveShare e-ink 2.13" V4 |
| **Resolution** | 250×122 pixels (landscape) |
| **Colors** | Black & White (1-bit) |
| **OS** | DietPi Trixie (Debian 13) |
| **Python** | 3.13.5 |
| **Interface** | SPI |

### Pin Connections

The WaveShare 2.13" V4 display connects to the Raspberry Pi GPIO pins via SPI. Ensure proper connection before powering on.

## ✨ Features

### DietpinkDisplay Wrapper

The core of this project is the `DietpinkDisplay` class, which provides a high-level API for working with the e-ink display:

- **Drawing Primitives**
  - Text rendering with multiple font sizes (tiny, small, medium, large, huge)
  - Text alignment (left, center, right)
  - Rectangles (filled or outlined)
  - Lines (customizable width)
  - Circles (filled or outlined)
  - Progress bars with customizable colors

- **Display Features**
  - Full refresh (complete screen update)
  - Partial refresh (faster updates, less ghosting)
  - Auto sleep mode for power saving
  - Context manager support for automatic cleanup
  - Image loading from files
  - Text size calculation

- **Developer Friendly**
  - Intuitive API design
  - Automatic font loading
  - Error handling
  - Built-in test suite
  - Extensive code comments

## 📂 Project Structure

```
dietpink/
├── README.MD                    # This file
├── docs/                        # Documentation
├── software/
│   └── eink/
│       ├── dietpink_display.py  # Main wrapper class
│       ├── drivers/             # WaveShare driver library
│       │   └── e-Paper/
│       └── examples/            # Example applications
│           └── clock.py         # Digital clock example
├── tests/                       # Unit and integration tests
│   └── eink/
├── scripts/                     # Utility scripts
├── configs/                     # Configuration files
├── hardware/                    # Hardware schematics and docs
└── logs/                        # Application logs
```

## 🚀 Quick Start

### Prerequisites

1. Raspberry Pi Zero W with DietPi installed
2. WaveShare e-ink 2.13" V4 display properly connected
3. SSH access enabled
4. Python 3.13+ installed

### Installation

1. **On your local machine:**
   ```bash
   cd ~/Maker-Projects
   git clone <your-repo-url>
   cd dietpink
   ```

2. **Deploy to Raspberry Pi:**
   ```bash
   # If you have a sync script
   ./scripts/sync.sh
   
   # Or manually using rsync
   rsync -avz --exclude 'logs/' --exclude '__pycache__/' \
     . root@dietpink.local:/root/projects/dietpink/
   ```

3. **Install dependencies on the Pi:**
   ```bash
   ssh root@dietpink.local
   pip3 install --break-system-packages Pillow spidev lgpio gpiozero qrcode
   ```

### Running Your First Example

```bash
ssh root@dietpink.local
cd /root/projects/dietpink/software/eink/examples
python3 clock.py
```

Press `Ctrl+C` to stop the example.

## 📱 Examples

### Currently Available

- ✅ **`clock.py`** - Digital clock with date and time
  - Updates every second using partial refresh
  - Shows day, date, and time
  - Minimal flickering thanks to partial refresh

### Planned Examples

The following examples are referenced in the project but not yet implemented:

- 📋 `boot_screen.py` - Startup screen with system info
- 📊 `dashboard.py` - System stats dashboard (CPU, memory, disk)
- 💻 `system_info.py` - Detailed system information
- 💬 `message.py` - Simple message display
- 🌤️ `weather.py` - Weather information display
- ✅ `todo.py` - Task list display
- 📱 `qr_display.py` - QR code generator and display

### Creating Your Own Display

Here's a simple example to get started:

```python
from dietpink_display import DietpinkDisplay
import time

# Use context manager for automatic cleanup
with DietpinkDisplay() as display:
    # Clear the canvas
    display.clear()
    
    # Draw a header
    display.rectangle(0, 0, 250, 30, fill=display.BLACK)
    display.text("Hello World!", 125, 5, size='large', 
                 color=display.WHITE, align='center')
    
    # Add some content
    display.text("Welcome to dietpink", 10, 45, size='medium')
    display.progress_bar(10, 70, 200, 15, 75)
    
    # Update the physical display
    display.refresh()
    
    # Sleep for 5 seconds
    time.sleep(5)
    
# Display automatically goes to sleep mode when exiting context
```

## 🔧 Development Workflow

### Syncing to Raspberry Pi

**Option 1: Using the sync script (recommended)**

From the Maker-Projects root directory:
```bash
./dietpink/scripts/sync.sh
```

This script will:
- ✅ Verify SSH connection to `dietpink`
- 🔄 Sync all project files using rsync
- 🚫 Automatically exclude unnecessary files (logs, cache, git files)
- 📊 Show progress during transfer

**Option 2: Manual rsync**

```bash
# From the Maker-Projects root directory
rsync -avz --delete \
    --exclude '__pycache__/' \
    --exclude 'logs/' \
    --exclude '.git/' \
    dietpink/ root@dietpink.local:/root/projects/dietpink/
```

### Development Cycle

1. **Edit code locally** on your development machine:
   ```bash
   cd ~/Maker-Projects/dietpink/software/eink
   # Edit files with your favorite editor
   ```

2. **Sync to Raspberry Pi**:
   ```bash
   # From Maker-Projects root
   ./dietpink/scripts/sync.sh
   ```

3. **Test on device**:
   ```bash
   ssh root@dietpink.local
   cd /root/projects/dietpink/software/eink/examples
   python3 clock.py
   ```

### Testing

Run the built-in wrapper test:
```bash
python3 dietpink_display.py
```

This will run through a series of tests showing text, shapes, progress bars, and a sample dashboard.

## 📚 API Reference

### DietpinkDisplay Class

#### Properties
- `WIDTH` - Display width in pixels (122)
- `HEIGHT` - Display height in pixels (250)
- `WHITE` - White color constant (255)
- `BLACK` - Black color constant (0)

#### Methods

**`__init__()`**
- Initialize the display and load fonts

**`clear(color=WHITE)`**
- Clear the canvas (does not update physical display)

**`text(text, x, y, size='medium', color=BLACK, align='left')`**
- Draw text on the canvas
- Sizes: 'tiny', 'small', 'medium', 'large', 'huge'
- Alignment: 'left', 'center', 'right'

**`rectangle(x, y, width, height, fill=None, outline=None, width_line=1)`**
- Draw a rectangle

**`line(x1, y1, x2, y2, color=BLACK, width=1)`**
- Draw a line

**`circle(x, y, radius, fill=None, outline=None, width=1)`**
- Draw a circle centered at (x, y)

**`progress_bar(x, y, width, height, percentage, bg_color=WHITE, fill_color=BLACK, border=True)`**
- Draw a progress bar (0-100%)

**`image_from_file(path, x, y, width=None, height=None)`**
- Load and display an image

**`refresh(partial=False)`**
- Update the physical display
- Use `partial=True` for faster updates

**`sleep()`**
- Put display in low-power sleep mode

**`clear_display()`**
- Clear the physical display (set to white)

**`get_text_size(text, size='medium')`**
- Returns (width, height) of text in pixels

## 📦 Dependencies

Install on the Raspberry Pi:

```bash
pip3 install --break-system-packages Pillow spidev lgpio gpiozero qrcode
```

### Required Libraries

- **Pillow** - Python Imaging Library for image manipulation
- **spidev** - SPI interface for display communication
- **lgpio** - GPIO control for Raspberry Pi
- **gpiozero** - High-level GPIO library
- **qrcode** - QR code generation (for QR examples)

### System Requirements

- DietPi Trixie (Debian 13) or Raspberry Pi OS
- SPI interface enabled (`raspi-config` → Interface Options → SPI)
- Python 3.13+

## 🔍 Troubleshooting

### Display not responding
- Check SPI is enabled: `raspi-config` → Interface Options → SPI
- Verify physical connections
- Run the test script: `python3 dietpink_display.py`

### Import errors
- Ensure you're on the Raspberry Pi (not local machine)
- Install all dependencies
- Check Python version: `python3 --version`

### Ghosting on display
- Use `display.clear_display()` for a full physical clear
- Perform a full refresh occasionally: `display.refresh(partial=False)`

### Permission errors
- The display requires GPIO access, typically need root or gpio group
- Try with sudo: `sudo python3 your_script.py`

### ModuleNotFoundError: waveshare_epd
- Check the driver path in `dietpink_display.py` matches your installation
- Default path: `/root/projects/dietpink/software/eink/drivers/e-Paper/RaspberryPi_JetsonNano/python/lib`

## 🎯 Future Enhancements

- [ ] Web interface for remote control
- [ ] Configuration file support
- [ ] More example applications
- [ ] Auto-rotation support
- [ ] Multi-display support
- [ ] Integration with APIs (weather, calendar, etc.)
- [ ] Animation framework
- [ ] Battery level monitoring
- [ ] Touch input support (if hardware added)

## 📄 License

Open source - available for personal and educational use.

## 👤 Author

dietpink project - 2025

## 🤝 Contributing

Part of the larger Maker-Projects repository. See the [main README](../README.md) for contribution guidelines.

---

**Happy coding!** 🎨✨ If you create something cool with dietpink, share it!