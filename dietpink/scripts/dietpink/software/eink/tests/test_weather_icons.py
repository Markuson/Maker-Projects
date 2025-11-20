#!/usr/bin/env python3
"""
Test de totes les icones meteorològiques
Mostra cada icona durant 3 segons
"""

import sys
import time

sys.path.append('/root/projects/dietpink/software/eink/modules')


from weather_ui import WeatherUI

# Tots els símbols YR possibles
symbols_to_test = [
    ('clearsky_day', 'Sol clar'),
    ('fair_day', 'Sol lleuger'),
    ('partlycloudy_day', 'Parcialment núvol'),
    ('cloudy', 'Núvol'),
    ('rain', 'Pluja'),
    ('lightrain', 'Pluja lleugera'),
    ('heavyrain', 'Pluja forta'),
    ('snow', 'Neu'),
    ('sleet', 'Aiguaneu'),
    ('fog', 'Boira'),
]

def main():
    print("🧪 Test de totes les icones meteorològiques")
    print("=" * 50)
    print("")
    
    ui = WeatherUI()
    
    # Temperatures de test fixes
    temp_interior = 21.5
    temp_exterior = 8.2
    
    for symbol_code, description in symbols_to_test:
        print(f"📊 Mostrant: {description} ({symbol_code})")
        
        # Crear previsió de test
        forecast = {
            'symbol_code': symbol_code,
            'precipitation': 2.5,
            'temperature_max': 15,
            'temperature_min': 8,
            'wind_speed': 3.5,
            'wind_direction': 90,
            'success': True
        }
        
        # Renderitzar
        ui.render(temp_interior, temp_exterior, forecast)
        
        print(f"   ⏳ Esperant 3 segons...")
        time.sleep(3)
        print("")
    
    print("🧹 Netejant display...")
    ui.clear()
    
    print("✅ Test completat!")
    print("")
    print("Icones testejades:")
    for symbol_code, description in symbols_to_test:
        print(f"  • {description}")

if __name__ == "__main__":
    main()
