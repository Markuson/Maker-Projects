#!/usr/bin/env python3
"""
weather_ha.py - Display meteorològic integrat
Mostra temperatures de Home Assistant + previsió YR al display e-ink

Arquitectura:
- MQTT: Temperatures en temps real (on-demand)
- YR API: Previsió cada 3h (00:00, 03:00, 06:00, etc.)
- UI: Update quan canvien dades
"""

import sys
import json
import time
import requests
import signal
from datetime import datetime, timedelta
from threading import Thread, Event

# Afegir paths dels mòduls
sys.path.append('/root/projects/dietpink/software/eink/modules')

from mqtt_handler import MQTTHandler
from yr_weather import YRWeatherClient
from weather_ui import WeatherUI


class WeatherDisplay:
    """Gestor principal del display meteorològic"""
    
    def __init__(self, config_path):
        """
        Inicialitzar sistema
        
        Args:
            config_path: Ruta al fitxer weather_config.json
        """
        print("🚀 Iniciant Weather Display...")
        print("=" * 50)
        
        # Carregar configuració
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Estat del sistema
        self.running = True
        self.shutdown_event = Event()
        
        # Dades actuals
        self.temp_interior = 0.0
        self.temp_exterior = 0.0
        self.forecast = None
        self.coordinates = None
        
        # Mòduls
        self.ui = None
        self.mqtt = None
        self.yr_client = None
        
        # Timestamps
        self.last_display_update = None
        self.last_yr_update = None
        
        print("✅ Configuració carregada")
    
    def setup(self):
        """Configurar tots els mòduls"""
        
        # 1. Obtenir coordenades de Home Assistant
        print("\n📍 Obtenint coordenades de Home Assistant...")
        if not self._get_coordinates():
            print("⚠️  No s'han pogut obtenir coordenades, usant Uppsala per defecte")
            self.coordinates = (59.8586, 17.6389)
        
        # 2. Inicialitzar UI
        print("\n🖼️  Inicialitzant UI...")
        self.ui = WeatherUI()
        print("✅ UI ready")
        
        # 3. Inicialitzar YR client
        print("\n🌤️  Inicialitzant YR Weather client...")
        self.yr_client = YRWeatherClient(
            user_agent=self.config['yr_api']['user_agent'],
            lat=self.coordinates[0],
            lon=self.coordinates[1]
        )
        print("✅ YR client ready")
        
        # 4. Obtenir primera previsió
        print("\n🌐 Obtenint previsió inicial...")
        self.forecast = self.yr_client.get_forecast()
        
        # 5. Inicialitzar MQTT
        print("\n📡 Inicialitzant MQTT handler...")
        mqtt_config = self.config['mqtt']
        self.mqtt = MQTTHandler(
            broker=mqtt_config['broker'],
            port=mqtt_config['port'],
            username=mqtt_config['username'],
            password=mqtt_config['password'],
            topics=mqtt_config['topics']
        )
        
        # Configurar callback MQTT
        self.mqtt.set_data_callback(self._on_temperature_change)
        
        # Connectar MQTT
        if self.mqtt.connect():
            print("✅ MQTT connectat")
        else:
            print("❌ Error connectant MQTT")
            return False
        
        # 6. Esperar primers missatges MQTT (màxim 5 segons)
        print("\n⏳ Esperant temperatures inicials...")
        time.sleep(5)
        self.temp_interior, self.temp_exterior = self.mqtt.get_temperatures()
        
        # 7. Mostrar UI inicial
        print("\n🎨 Renderitzant UI inicial...")
        self._update_display()
        
        print("\n" + "=" * 50)
        print("✅ Sistema inicialitzat correctament!")
        print("=" * 50)
        
        return True
    
    def _get_coordinates(self):
        """Obtenir coordenades de Home Assistant API"""
        try:
            headers = {
                'Authorization': f"Bearer {self.config['homeassistant']['token']}",
                'Content-Type': 'application/json'
            }
            
            url = f"{self.config['homeassistant']['url']}/api/config"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            config = response.json()
            lat = config['latitude']
            lon = config['longitude']
            
            self.coordinates = (lat, lon)
            print(f"   ✅ Coordenades: ({lat}, {lon})")
            return True
            
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
            return False
    
    def _on_temperature_change(self, temp_balco, temp_menjador):
        """
        Callback quan canvien les temperatures via MQTT
        
        Args:
            temp_balco: Temperatura exterior
            temp_menjador: Temperatura interior
        """
        print(f"\n🔔 Temperatures actualitzades: IN={temp_menjador}°C, OUT={temp_balco}°C")
        
        self.temp_interior = temp_menjador
        self.temp_exterior = temp_balco
        
        # Update display
        self._update_display()
    
    def _update_display(self):
        """Actualitzar display amb dades actuals"""
        try:
            print("🎨 Actualitzant display...")
            print(f"   DEBUG: temp_interior={self.temp_interior}")
            print(f"   DEBUG: temp_exterior={self.temp_exterior}")
            print(f"   DEBUG: forecast={self.forecast}")
            
            # Usar última previsió en cache si no n'hi ha
            if self.forecast is None:
                print("   ⚠️  Forecast is None, obtenint cached...")
                self.forecast = self.yr_client.get_cached_forecast()
                print(f"   DEBUG: cached forecast={self.forecast}")
            
            # Renderitzar
            print("   Cridant ui.render()...")
            self.ui.render(
                temp_interior=self.temp_interior,
                temp_exterior=self.temp_exterior,
                forecast=self.forecast
            )
            
            self.last_display_update = datetime.now()
            print("   ✅ Display actualitzat (render completat)")
            
        except Exception as e:
            print(f"   ❌ Error actualitzant display: {e}")
            import traceback
            traceback.print_exc()

    def _should_update_yr(self):
        """Comprovar si cal actualitzar previsió YR (cada 3h)"""
        if self.last_yr_update is None:
            return True
        
        now = datetime.now()
        elapsed = now - self.last_yr_update
        
        # Actualitzar cada 3 hores
        interval = timedelta(hours=self.config['yr_api']['update_interval_hours'])
        
        if elapsed >= interval:
            # Comprovar si estem a una hora "rodona" (00:00, 03:00, 06:00, etc.)
            if now.hour % self.config['yr_api']['update_interval_hours'] == 0:
                return True
        
        return False
    
    def _yr_update_loop(self):
        """Thread per actualitzar YR periòdicament"""
        print("\n🔄 Thread YR iniciat")
        
        while self.running:
            try:
                if self._should_update_yr():
                    print(f"\n⏰ Update programat YR ({datetime.now().strftime('%H:%M')})")
                    
                    new_forecast = self.yr_client.get_forecast()
                    
                    if new_forecast['success']:
                        self.forecast = new_forecast
                        self.last_yr_update = datetime.now()
                        
                        # Update display amb nova previsió
                        self._update_display()
                    else:
                        print("   ⚠️  Previsió fallida, mantenint anterior")
                
                # Comprovar cada 10 minuts
                self.shutdown_event.wait(600)
                
            except Exception as e:
                print(f"❌ Error al thread YR: {e}")
                self.shutdown_event.wait(600)
    
    def run(self):
        """Executar loop principal"""
        
        # Iniciar thread YR
        yr_thread = Thread(target=self._yr_update_loop, daemon=True)
        yr_thread.start()
        
        print("\n🏃 Sistema en execució...")
        print("   Prem Ctrl+C per aturar")
        print("")
        
        try:
            # Loop principal (només mantenir viu)
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Interrupció rebuda (Ctrl+C)")
            self.shutdown()
    
    def shutdown(self):
        """Aturar sistema correctament"""
        print("\n🛑 Aturant sistema...")
        
        self.running = False
        self.shutdown_event.set()
        
        # Desconnectar MQTT
        if self.mqtt:
            self.mqtt.disconnect()
        
        # Netejar display (opcional)
        # self.ui.clear()
        
        print("✅ Sistema aturat correctament")
        print("")


def main():
    """Punt d'entrada principal"""
    
    # Ruta configuració
    config_path = '/root/projects/dietpink/software/eink/config/weather_config.json'
    
    # Crear sistema
    weather = WeatherDisplay(config_path)
    
    # Configurar signal handler per Ctrl+C
    def signal_handler(sig, frame):
        weather.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Setup
    if not weather.setup():
        print("❌ Error durant setup")
        sys.exit(1)
    
    # Run
    weather.run()


if __name__ == "__main__":
    main()
