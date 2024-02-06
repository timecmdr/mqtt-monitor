import paho.mqtt.client as mqtt
import os
import configparser

# Load MQTT configuration from file
config = configparser.ConfigParser()
config.read('mqtt-monitor.config')

mqtt_broker = config['mqtt']['broker_ip']
mqtt_port = int(config['mqtt']['port'])
mqtt_username = config['mqtt']['username']
mqtt_password = config['mqtt']['password']

# MQTT Topics
input1_topic = "/home/monitor/switchtoDP1"
input2_topic = "/home/monitor/switchtoDP2"

# Bash commands
input1_command = "ddcutil setvcp 60 0x0f"
input2_command = "ddcutil setvcp 60 0x10"

# MQTT callback when message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')

    if topic == input1_topic:
        print(f"Received message on {input1_topic}: {payload}")
        os.system(input1_command)
    elif topic == input2_topic:
        print(f"Received message on {input2_topic}: {payload}")
        os.system(input2_command)

# MQTT callback when connected to broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to MQTT topics on successful connection
    client.subscribe([(input1_topic, 0), (input2_topic, 0)])

# Create MQTT client
client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=mqtt_password)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Start the MQTT loop
client.loop_forever()
