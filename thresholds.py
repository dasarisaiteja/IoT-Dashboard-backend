# Limits for the sensors
# If the value is too high or too low, it's bad

# Temperature limits
TEMP_MIN = -10.0
TEMP_MAX = 80.0

# Humidity limits
HUMID_MIN = 10.0
HUMID_MAX = 95.0

# Voltage limits
VOLT_MIN = 210.0
VOLT_MAX = 250.0

# Current limits
CURR_MIN = 0.0
CURR_MAX = 15.0

# Pressure limits
PRESS_MIN = 900.0
PRESS_MAX = 1100.0

def check_thresholds(data):
    # This list will hold the errors we find
    problems = []
    
    # 1. Check Temperature
    if "temperature" in data:
        t_val = data["temperature"]
        if t_val != None:
            if t_val < TEMP_MIN or t_val > TEMP_MAX:
                # Add to problems list
                p = {}
                p["key"] = "temperature"
                p["actual"] = t_val
                p["min_allowed"] = TEMP_MIN
                p["max_allowed"] = TEMP_MAX
                problems.append(p)
                
    # 2. Check Humidity
    if "humidity" in data:
        h_val = data["humidity"]
        if h_val != None:
            if h_val < HUMID_MIN or h_val > HUMID_MAX:
                p = {}
                p["key"] = "humidity"
                p["actual"] = h_val
                p["min_allowed"] = HUMID_MIN
                p["max_allowed"] = HUMID_MAX
                problems.append(p)

    # 3. Check Voltage
    if "voltage" in data:
        v_val = data["voltage"]
        if v_val != None:
            if v_val < VOLT_MIN or v_val > VOLT_MAX:
                p = {}
                p["key"] = "voltage"
                p["actual"] = v_val
                p["min_allowed"] = VOLT_MIN
                p["max_allowed"] = VOLT_MAX
                problems.append(p)

    # 4. Check Current
    if "current" in data:
        c_val = data["current"]
        if c_val != None:
            if c_val < CURR_MIN or c_val > CURR_MAX:
                p = {}
                p["key"] = "current"
                p["actual"] = c_val
                p["min_allowed"] = CURR_MIN
                p["max_allowed"] = CURR_MAX
                problems.append(p)

    # 5. Check Pressure
    if "pressure" in data:
        pr_val = data["pressure"]
        if pr_val != None:
            if pr_val < PRESS_MIN or pr_val > PRESS_MAX:
                p = {}
                p["key"] = "pressure"
                p["actual"] = pr_val
                p["min_allowed"] = PRESS_MIN
                p["max_allowed"] = PRESS_MAX
                problems.append(p)
                
    return problems