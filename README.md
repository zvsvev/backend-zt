# Farm Management Web & IoT System

Welcome to the Farm Management System. This project bridges top-level web API interfaces with low-level industrial IoT (Internet of Things) devices using Modbus protocol. It is driven by a PostgreSQL database schema specifically designed for modern farms (Kandang, Lantai) and hardware actuators (Blowers, Dimmers, Heaters, Pumps).

This repository contains:
1. A **FastAPI** web backend with automatically generated Swagger UI.
2. A **PyModbus** daemon script acting as an IoT Gateway between PostgreSQL and physical actuators.

---

## The Architecture & Synchronization
The system works through two-way IoT synchronization:
1. **Reading from Hardware:** The Python gateway uses PyModbus to read electrical holding registers from hardware (e.g., current temperature). It then connects to PostgreSQL and runs an `UPDATE actuator` query. The Swagger UI reflects this new live data.
2. **Writing to Hardware:** A user updates an Actuator's config (e.g. Blower `max_temperature`) via the Swagger UI. The gateway script constantly polls the database. When it sees an update, it sends a `write_register` signal to update the local memory bank on the physical farm hardware.

---

## How to Test and Run Locally (End-to-End Simulation)

To perform a complete test of the system on your local machine, you will need 4 separate terminal windows to run each micro-component identically to a real production farm environment.

### Terminal 1: Spin up the PostgreSQL Database
You need a database running for the API to connect to. We have provided a `docker-compose.yml` to spin it up instantly without manual installation.
Run this command:
```bash
docker compose up -d
```
*(This starts a Postgres database in the background on port 5432 with the expected user/password).*

### Terminal 2: Run the FastAPI Web Server
With the database running, launch your web API framework. First, install the requirements if you haven't:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
You can now open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view the Auto-Generated Swagger Interface based on your database ERD. Feel free to use the `POST` endpoints here to create some mock Actuators so the database has rows to sync!

### Terminal 3: Power On the Mock Hardware
Since you likely don't have physical PLCs and actuators wired to your laptop, run our mock hardware script. This acts exactly like a physical hardware sensor sitting on the farm.
```bash
python3 mock_modbus_server.py
```

### Terminal 4: Start the IoT Gateway (The "PyModbus Test")
Finally, run the Modbus bridging daemon! This script reads from your database (Terminal 2) and writes to the hardware (Terminal 3), and vice versa. 
```bash
python3 modbus_gateway.py
```

**Testing the Flow:**
Go to your Swagger UI (`localhost:8000/docs`). Find the Blower Config PUT endpoint, change the `max_temperature`, and watch Terminal 4 instantly log that it passed that exact configuration down perfectly to the mock hardware!

---

## Vercel Deployment Note
If you want to deploy this API to the cloud using Vercel, Vercel will auto-read our `vercel.json` file and host the FastAPI application (`main.py`) flawlessly! 

However, **do NOT deploy the `modbus_gateway.py` script to Vercel**. Vercel uses "Serverless Functions" which spin up and die in milliseconds; they are strictly designed to handle web server API requests. The IoT PyModbus gateway is a "daemon" containing a `while True:` loop. It must run indefinitely on a machine that stays constantly powered on (like a Raspberry Pi sitting on the farm, or an EC2 instance), pointing it to your remote Database URL.
