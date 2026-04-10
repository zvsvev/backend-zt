# Farm Management Web & IoT System

Welcome to the Farm Management System. This project bridges top-level web API interfaces with low-level industrial IoT (Internet of Things) devices using Modbus protocol. It is driven by a PostgreSQL database schema specifically designed for modern farms (Kandang, Lantai) and hardware actuators (Blowers, Dimmers, Heaters, Pumps).

This guide explains how to use both the **Swagger UI REST API setup** and the **PyModbus IoT integration**.

---

## Part 1: How the Swagger UI Works

The Swagger UI provides a visual, interactive interface to view and test your REST API endpoints. Instead of using tools like Postman, you can use Swagger UI to directly interact with your database using standard HTTP methods (GET, POST, PUT, DELETE).

### 1. The OpenAPI Specification (`openapi.yaml`)
We designed an OpenAPI 3.0 configuration file (`openapi.yaml`). This file translates your exact database Entity-Relationship Diagram (ERD) into RESTful endpoints:
- **/kandang & /lantai:** Manage the structure and locations of the farm.
- **/actuators:** View live states (`current_status`, `current_value`) of farm hardware mapped via UUIDs.
- **/actuators/{uuid}/*_config**: Set thresholds (like `min_temperature`, `interval_on_duration`) for blowers, heaters, dimmers, and pumps.
- **/audit_logs:** Track when configurations are modified.

### 2. The User Interface (`index.html`)
The `index.html` file acts as the host client. It loads the official Swagger UI libraries through a CDN, applies a customized dark-mode/light-mode experience, and mounts the endpoints specified in `openapi.yaml`.

### 3. How to Run and Test
Since `index.html` fetches the YAML file locally, you need a local server to avoid CORS issues:

1. Open your terminal in this directory.
2. Run a simple Python web server:
   ```bash
   python3 -m http.server 3000
   ```
3. Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)**.
4. From here, you can click on endpoints, click "Try it out", and see what standard JSON payloads the API requires based on your database ERD.

---

## Part 2: How to Try PyModbus (IoT Gateway)

The web API alone cannot talk to physical hardware; Modbus is the standard industrial language used by Actuators and PLCs. To bridge the Postgres database and the physical Modbus devices, we use **PyModbus**.

We accomplish this through a "Daemon Gateway" script (`modbus_gateway.py`), which runs endlessly in the background.

### The Two-Way Synchronization Concept

1. **Reading from Hardware:** The Python gateway uses PyModbus to read electrical holding registers from your hardware (e.g., current temperature). It then connects to PostgreSQL using `psycopg2` and runs an `UPDATE actuator SET current_value = X` query. The Swagger UI will now reflect this new data!
2. **Writing to Hardware:** A user updates a Blower's `max_temperature` limit via the Swagger UI. The gateway script constantly polls the `blower_config` table. When it sees the update, it uses PyModbus to send a `write_register` signal to update the local memory bank on the physical farm hardware.

### Prerequisites to Run PyModbus
Make sure your environment is prepared by installing the required modbus and database drivers:

```bash
pip install pymodbus psycopg2-binary
```

*(Note: Depending on your Python configuration, you might need to use `pip3`)*

### How to Test / Simulate It

If you don't have a physical Blower or Heater connected to your local network, you can still test it cleanly!

1. **Setup the Database:** Ensure you have PostgreSQL running with a database named `farm_db` that contains the tables described in your ERD (`actuator`, `blower_config`, etc).
2. **Update the Gateway Credentials:** Open `modbus_gateway.py` and ensure `DB_USER` and `DB_PASSWORD` align with your local Postgres configuration.
3. **Run a Mock Modbus Server**: In a separate terminal, install a modbus server to simulate the hardware:
   *(PyModbus syntax varies slightly between v2 and v3. Consult PyModbus official examples to run a synchronous mock server simulating `localhost:502`).
4. **Execute the Gateway:** Run the bridge script:
   ```bash
   python3 modbus_gateway.py
   ```

Watch your terminal. The script will securely bridge the gap, printing logs every 5 seconds as it passes settings back and forth between the high-level PostgreSQL system and the low-level Modbus hardware.
