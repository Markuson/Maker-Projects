#!/usr/bin/env python3
"""
mqtt_handler.py - Gestor de connexions MQTT
Subscriu a topics de temperatura i gestiona callbacks
"""

import paho.mqtt.client as mqtt
from threading import Lock


class MQTTHandler:
    """Gestor de connexions MQTT per dietpink"""
    
    def __init__(self, broker, port, username, password, topics):
        """
        Inicialitzar handler MQTT
        
        Args:
            broker: IP/hostname del broker MQTT
            port: Port del broker (normalment 1883)
            username: Usuari MQTT
            password: Password MQTT
            topics: dict amb topics a subscriure
        """
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topics = topics
        
        # Dades rebudes
        self.data = {
            'temp_balco': None,
            'temp_menjador': None
        }
        self.data_lock = Lock()
        
        # Callbacks externs
        self.on_data_callback = None
        
        # Client MQTT
        self.client = mqtt.Client(
            client_id="dietpink_weather",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1
        )
        self.client.username_pw_set(username, password)
        
        # Configurar callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        self.connected = False
    
    def connect(self):
        """Connectar al broker MQTT"""
        try:
            print(f"🔌 MQTT: Connectant a {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"❌ MQTT: Error connexió: {e}")
            return False
    
    def disconnect(self):
        """Desconnectar del broker"""
        print("🔌 MQTT: Desconnectant...")
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
    
    def set_data_callback(self, callback):
        """
        Establir callback quan arriben dades noves
        
        Args:
            callback: funció a cridar quan canvia temperatura
                     Signatura: callback(balco, menjador)
        """
        self.on_data_callback = callback
    
    def get_temperatures(self):
        """
        Obtenir temperatures actuals
        
        Returns:
            tuple: (temp_balco, temp_menjador)
        """
        with self.data_lock:
            return (self.data['temp_balco'], self.data['temp_menjador'])
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback quan es connecta al broker"""
        if rc == 0:
            print("✅ MQTT: Connectat!")
            self.connected = True
            
            # Subscriure's als topics
            for key, topic in self.topics.items():
                client.subscribe(topic)
                print(f"📡 MQTT: Subscrit a {topic}")
        else:
            print(f"❌ MQTT: Error connexió (codi {rc})")
            self.connected = False
    
    def _on_message(self, client, userdata, msg):
        """Callback quan arriba un missatge"""
        topic = msg.topic
        payload = msg.payload.decode()
        
        try:
            value = float(payload)
            changed = False
            
            with self.data_lock:
                if topic == self.topics.get('balco'):
                    old_value = self.data['temp_balco']
                    self.data['temp_balco'] = value
                    print(f"🌡️  MQTT: Balcó = {value}°C")
                    
                    if old_value is None or abs(value - old_value) >= 0.1:
                        changed = True
                
                elif topic == self.topics.get('menjador'):
                    old_value = self.data['temp_menjador']
                    self.data['temp_menjador'] = value
                    print(f"🏠 MQTT: Menjador = {value}°C")
                    
                    if old_value is None or abs(value - old_value) >= 0.1:
                        changed = True
            
            # Cridar callback fora del lock
            if changed:
                self._trigger_callback()
        
        except ValueError:
            print(f"⚠️  MQTT: Valor no numèric: {payload}")
        except Exception as e:
            print(f"⚠️  MQTT: Error processant missatge: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback quan es desconnecta"""
        self.connected = False
        if rc != 0:
            print("⚠️  MQTT: Desconnexió inesperada. Reconnectant...")
    
    def _trigger_callback(self):
        """Cridar callback extern si està definit"""
        if self.on_data_callback:
            try:
                temps = self.get_temperatures()
                self.on_data_callback(temps[0], temps[1])
            except Exception as e:
                print(f"⚠️  MQTT: Error al callback: {e}")


# Test del mòdul
if __name__ == "__main__":
    import json
    import time
    
    # Carregar config
    config_path = '/root/projects/dietpink/software/eink/config/weather_config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    mqtt_config = config['mqtt']
    
    # Callback de test
    def on_data_change(balco, menjador):
        print(f"\n🔔 Callback: Balcó={balco}°C, Menjador={menjador}°C\n")
    
    # Crear handler
    handler = MQTTHandler(
        broker=mqtt_config['broker'],
        port=mqtt_config['port'],
        username=mqtt_config['username'],
        password=mqtt_config['password'],
        topics=mqtt_config['topics']
    )
    
    handler.set_data_callback(on_data_change)
    
    # Connectar
    if handler.connect():
        print("\n⏳ Esperant missatges (Ctrl+C per aturar)...\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Test aturat")
            handler.disconnect()
