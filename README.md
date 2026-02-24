# My IoT Project - Sensor Dashboard

This is my project for the IoT dashboard. It uses Python and FastAPI to show data from sensors. The data comes from MQTT and goes into a MySQL database.

## What is in this project?
* **main.py**: This is where the app starts.
* **database.py**: This handles the connection to MySQL.
* **mqtt_client.py**: This part listens to the sensor messages.
* **thresholds.py**: This is where I set the limits for the alarms.
* **routers/**: This folder has the API links for the frontend.

## How to run it

### 1. Requirements
You need to have Docker and Docker Compose installed on your computer.

### 2. Steps to start
First, you need to build the container. Open your terminal and type:
`docker-compose build`

After it finishes building, you can start everything with this command:
`docker-compose up`

### 3. Checking the API
Once it is running, you can go to your browser and see the documentation here:
`http://localhost:8000/docs`

You can click "Try it out" to see if the data is coming from the database.

## Things I want to add later
* Make a login page for users.
* Add more sensors to the list.
* Make the dashboard look better with colors.