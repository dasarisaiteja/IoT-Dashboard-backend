import asyncio
import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt

from database import SessionLocal, SensorReading, Alert
from thresholds import check_thresholds

# --- SETTINGS ---

# Get values from the environment or use defaults
host = os.getenv("MQTT_BROKER_HOST", "mosquitto")
port_str = os.getenv("MQTT_BROKER_PORT", "1883")
port = int(port_str)
user = os.getenv("MQTT_USERNAME", "")
pw = os.getenv("MQTT_PASSWORD", "")

# The list of topics to listen to
my_topics = [
    "sensors/device001/data",
    "sensors/device002/data",
    "sensors/device003/data",
    "sensors/device004/data",
    "sensors/device005/data",
    "factory/floor1/sensors",
    "factory/floor2/sensors",
    "building/room101/environment",
    "building/room102/environment",
    "weather/outdoor/readings",
]

def save_sensor_reading(topic_name, message_data):
    # Get a database session
    db = SessionLocal()
    
    try:
        # Create a new reading object
        r = SensorReading()
        r.topic = topic_name
        r.temperature = message_data.get("temperature")
        r.humidity = message_data.get("humidity")
        r.voltage = message_data.get("voltage")
        r.current = message_data.get("current")
        r.pressure = message_data.get("pressure")
        # Turn dict into string for raw_json
        r.raw_json = json.dumps(message_data)
        r.received_at = datetime.utcnow()
        
        db.add(r)
        db.commit()
        print("Saved data to database")
        
        # Check for alerts now
        v_list = check_thresholds(message_data)
        
        if len(v_list) > 0:
            # We found some problems
            v_keys = ""
            actuals = {}
            limits = {}
            
            for v in v_list:
                # Build a string of names
                if v_keys == "":
                    v_keys = v["key"]
                else:
                    v_keys = v_keys + ", " + v["key"]
                
                # Store the values
                actuals[v["key"]] = v["actual"]
                
                # Store the limits
                limits_dict = {}
                limits_dict["min"] = v["min_allowed"]
                limits_dict["max"] = v["max_allowed"]
                limits[v["key"]] = limits_dict
            
            # Decide if it is critical or warning
            sev = "WARNING"
            if len(v_list) > 2:
                sev = "CRITICAL"
                
            # Create the alert
            new_alert = Alert()
            new_alert.topic = topic_name
            new_alert.violated_keys = v_keys
            new_alert.actual_values = json.dumps(actuals)
            new_alert.threshold_values = json.dumps(limits)
            new_alert.severity = sev
            new_alert.created_at = datetime.utcnow()
            
            db.add(new_alert)
            db.commit()
            print("Alert was created")
            
    except Exception as e:
        print("Something went wrong saving to db")
        print(e)
        db.rollback()
    finally:
        db.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected okay")
        # Subscribe to each topic in the list
        for t in my_topics:
            client.subscribe(t)
            print("Subscribed to " + t)
    else:
        print("Bad connection")

def on_message(client, userdata, msg):
    # Get the topic and the body
    t = msg.topic
    b = msg.payload.decode("utf-8")
    
    print("Got message on " + t)
    
    try:
        # Parse it
        parsed_data = json.loads(b)
        save_sensor_reading(t, parsed_data)
    except:
        print("Error parsing the message")

async def start_mqtt_client():
    print("Mqtt starting...")
    
    # Setup the client
    c = mqtt.Client("iot_dashboard_server")
    
    if user != "" and pw != "":
        c.username_pw_set(user, pw)
    
    c.on_connect = on_connect
    c.on_message = on_message
    
    while True:
        try:
            print("Trying to connect...")
            c.connect(host, port, 60)
            c.loop_start()
            
            # Just wait forever
            while True:
                await asyncio.sleep(1)
                
        except:
            print("Connection failed. Retrying in 5 seconds")
            await asyncio.sleep(5)