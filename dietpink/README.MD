# 🎨 dietpink

An e-ink dashboard for Raspberry Pi Zero W featuring a WaveShare 2.13" V4 display. A low-power, always-on information display perfect for desks, shelves, or anywhere you want glanceable information without the distraction of a backlit screen.

## 📋 Table of Contents

- [Overview](#overview)
- [Hardware Specifications](#hardware-specifications)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Weather Display System](#weather-display-system)
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
| **OS** | DietPi Bookworm (Debian 12) |
| **Python** | 3.11+ |
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
├── README.md                    # This file
├── docs/                        # Documentation
│   ├── DECISIONS.md             # Technical decisions
│   └── CHANGELOG.md             # Version history
├── software/
│   └── eink/
│       ├── dietpink_display.py  # Main wrapper class
│       ├── weather_ha.py        # Weather display main script
│       ├── manage.sh            # Service management script
│       ├── config/
│       │   ├── weather_config.json          # Configuration (gitignored)
│       │   └── weather_config.example.json  # Configuration template
│       ├── modules/             # Weather display modules
│       │   ├── __init__.py
│       │   ├── mqtt_handler.py  # Home Assistant MQTT client
│       │   ├── yr_weather.py    # YR.no weather API client
│       │   └── weather_ui.py    # E-ink UI renderer
│       ├── drivers/             # WaveShare driver library
│       │   └── e-Paper/
│       ├── examples/            # Example applications
│       │   └── clock.py         # Digital clock example
│       └── tests/               # Module tests
│           ├── test_mqtt_simple.py
│           ├── test_yr_uppsala.py
│           └── test_weather_icons.py
├── scripts/                     # Utility scripts
│   ├── sync.sh                  # Sync Pi → Mac
│   └── deploy.sh                # Deploy Mac → Pi
├── configs/                     # Configuration files
├── hardware/                    # Hardware schematics and docs
└── logs/                        # Application logs
```

## 🚀 Quick Start

### Prerequisites

1. Raspberry Pi Zero W with DietPi installed
2. WaveShare e-ink 2.13" V4 display properly connected
3. SSH access enabled
4. Python 3.11+ installed

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
   pip3 install --break-system-packages Pillow spidev lgpio gpiozero qrcode paho-mqtt requests
   ```

### Running Your First Example

```bash
ssh root@dietpink.local
cd /root/projects/dietpink/software/eink/examples
python3 clock.py
```

Press `Ctrl+C` to stop the example.

## 🌤️ Weather Display System

A complete weather monitoring system integrating Home Assistant sensors and YR.no forecast data.

### Features

- **Real-time indoor/outdoor temperatures** via Home Assistant MQTT
- **Weather forecast** from YR.no API (updated every 3 hours)
- **Graphical weather icons** rendered with PIL geometry
- **Wind direction indicator** with directional triangle
- **Auto-start service** via systemd
- **Automatic updates** on temperature changes

### Display Layout

```
┌─────────────────────────────┐
│   ┌────┐  │                 │
│   │22°C│  │   ☁️ (icon)     │
│   └────┘  │                 │
│  indoor   │                 │
│           │  Max: 15°C      │
│    8°C    │  Min: 8°C       │
│  outdoor  │  Rain: 2.3mm    │
│           │  12km/h ▲       │
└─────────────────────────────┘
```

### Architecture

```
weather_ha.py (main)
├── modules/mqtt_handler.py    # MQTT client for HA sensors
├── modules/yr_weather.py      # YR.no API client
└── modules/weather_ui.py      # Display rendering with icons
```

### Setup

1. **Configure Home Assistant MQTT**
   
   Create automations to publish temperature sensor values to MQTT topics:
   - `dietpink/temperatura/balco` (outdoor)
   - `dietpink/temperatura/menjador` (indoor)

2. **Create configuration file**
   ```bash
   cd /root/projects/dietpink/software/eink
   cp config/weather_config.example.json config/weather_config.json
   nvim config/weather_config.json
   ```
   
   Fill in:
   - `homeassistant.token`: Long-Lived Access Token from HA
   - `mqtt.password`: MQTT user password
   - `yr_api.user_agent`: Your email (required by YR API)

3. **Test modules individually**
   ```bash
   cd modules
   python3 mqtt_handler.py      # Test MQTT connection
   python3 yr_weather.py        # Test YR API
   python3 weather_ui.py        # Test display rendering
   ```

4. **Run the weather display**
   ```bash
   python3 weather_ha.py
   ```

5. **Install as systemd service**
   ```bash
   sudo cp dietpink-weather.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable dietpink-weather
   sudo systemctl start dietpink-weather
   ```

### Service Management

```bash
./manage.sh start     # Start service
./manage.sh stop      # Stop service
./manage.sh restart   # Restart service
./manage.sh status    # Check status
./manage.sh logs      # View live logs
```

### Weather Icons

The system renders graphical icons for each weather condition:

| Condition | Icon Description |
|-----------|------------------|
| Clear sky | Sun with rays |
| Partly cloudy | Sun + cloud |
| Cloudy | Rounded cloud |
| Rain | Cloud + droplets |
| Heavy rain | Cloud + thick lines |
| Snow | Cloud + snowflakes |
| Fog | Horizontal lines |

### Home Assistant Configuration

#### Creating MQTT User

1. **Settings** → **People** → **Users** tab
2. **Add User**
   - Name: `MQTT dietpink`
   - Username: `mqtt_dietpink`
   - Password: (choose and save)
   - ✅ Can only login from local network

#### Creating Temperature Automations

Example automation for outdoor temperature:

```yaml
alias: Publicar Temperatura Balcó
trigger:
  - platform: state
    entity_id: sensor.your_outdoor_sensor
action:
  - service: mqtt.publish
    data:
      topic: dietpink/temperatura/balco
      payload: "{{ states('sensor.your_outdoor_sensor') }}"
      retain: true
mode: single
```

#### Getting Long-Lived Access Token

1. Home Assistant → Click your profile (bottom left)
2. Scroll to **Long-Lived Access Tokens**
3. Click **Create Token**
4. Name: `dietpink_api`
5. Copy token to `weather_config.json`

## 📱 Examples

### Currently Available

- ✅ **`clock.py`** - Digital clock with date and time
  - Updates every second using partial refresh
  - Shows day, date, and time
  - Minimal flickering thanks to partial refresh

- ✅ **`weather_ha.py`** - Weather display with Home Assistant integration
  - Real-time temperatures via MQTT
  - YR.no weather forecast
  - Graphical weather icons
  - Systemd service support

### Planned Examples

- 📋 `boot_screen.py` - Startup screen with system info
- 📊 `dashboard.py` - System stats dashboard (CPU, memory, disk)
- 💻 `system_info.py` - Detailed system information
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
- 🚫 Automatically exclude unnecessary files (logs, cache, git files, secrets)
- 📊 Show progress during transfer

**Option 2: Deploy script (Mac → Pi with service restart)**

```bash
./dietpink/scripts/deploy.sh
```

This will sync files AND restart the systemd service automatically.

**Option 3: Manual rsync**

```bash
# From the Maker-Projects root directory
rsync -avz --delete \
    --exclude '__pycache__/' \
    --exclude 'logs/' \
    --exclude '.git/' \
    --exclude 'weather_config.json' \
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
   cd /root/projects/dietpink/software/eink
   python3 weather_ha.py
   ```

### Testing

Run individual module tests:
```bash
cd /root/projects/dietpink/software/eink

# Test display wrapper
python3 dietpink_display.py

# Test weather modules
python3 modules/mqtt_handler.py
python3 modules/yr_weather.py
python3 modules/weather_ui.py

# Test all weather icons
python3 tests/test_weather_icons.py
```

## 📚 API Reference

### DietpinkDisplay Class

#### Properties
- `WIDTH` - Display width in pixels (250)
- `HEIGHT` - Display height in pixels (122)
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

**`show_image(image)`**
- Display a PIL Image object directly

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
pip3 install --break-system-packages Pillow spidev lgpio gpiozero qrcode paho-mqtt requests
```

### Required Libraries

| Library | Purpose |
|---------|---------|
| **Pillow** | Image manipulation and drawing |
| **spidev** | SPI interface for display |
| **lgpio** | GPIO control for Raspberry Pi |
| **gpiozero** | High-level GPIO library |
| **qrcode** | QR code generation |
| **paho-mqtt** | MQTT client for Home Assistant |
| **requests** | HTTP client for YR.no API |

### System Requirements

- DietPi Bookworm (Debian 12) or Raspberry Pi OS
- SPI interface enabled (`dietpi-config` → Advanced Options → SPI)
- Python 3.11+

## 🔍 Troubleshooting

### Display not responding
- Check SPI is enabled: `dietpi-config` → Advanced Options → SPI
- Verify physical connections
- Run the test script: `python3 dietpink_display.py`

### Import errors
- Ensure you're on the Raspberry Pi (not local machine)
- Install all dependencies with `--break-system-packages` flag

### Weather display not updating
- Check MQTT connection: `python3 modules/mqtt_handler.py`
- Verify Home Assistant automations are triggering
- Check service logs: `./manage.sh logs`

### No temperatures received
- Manually trigger HA automations from the UI
- Verify MQTT credentials in `weather_config.json`
- Check Mosquitto broker is running in HA

### YR API errors
- Verify `user_agent` email is set in config
- Check internet connectivity
- API may be rate-limited, wait and retry

### Service won't start
```bash
# Check detailed logs
journalctl -u dietpink-weather -n 50

# Test manually
cd /root/projects/dietpink/software/eink
python3 weather_ha.py
```

## 📄 License

MIT License

## 👤 Author

Marc - 2025
