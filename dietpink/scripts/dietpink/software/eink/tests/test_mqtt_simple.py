#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

BROKER = "192.168.0.48"
PORT = 1883
USERNAME = "mqtt_dietpink"
PASSWORD = "dietpink-mqtt" 

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ CONNECTAT a Home Assistant MQTT!")
        client.subscribe("dietpink/#")
        print("📡 Escoltant dietpink/#...")
        print("")
    else:
        print(f"❌ ERROR connexió: {rc}")
        print("   Codis: 1=protocol, 3=servidor, 4=user/pass, 5=no autoritzat")

def on_message(client, userdata, msg):
    print(f"📨 REBUT: {msg.topic} = {msg.payload.decode()}")

client = mqtt.Client(client_id="dietpink_test")
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Connectant a MQTT broker...")

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    
    print("⏳ Esperant missatges (Ctrl+C per aturar)...")
    print("")
    
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n⏹️  Aturat")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"\n❌ Error: {e}")
    client.loop_stop()
    client.disconnect()
