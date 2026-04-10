import time
import psycopg2
from pymodbus.client import ModbusTcpClient

"""
Farm Management IoT Gateway Demo

This script bridges a physical or simulated Modbus device (Actuators/Sensors)
with the Farm Management PostgreSQL Database.

It demonstrates a two-way sync loop:
1. READ FROM MODBUS -> UPDATE DATABASE
2. READ FROM DATABASE -> WRITE TO MODBUS
"""

# ================= Configuration =================
# Database Connection (Adjust to match your PostgreSQL setup)
DB_HOST = "localhost"
DB_NAME = "farm_db"
DB_USER = "postgres"
DB_PASSWORD = "password"

# Modbus TCP Connection (Adjust to match your PLC/ESP32/Hardware)
MODBUS_HOST = "127.0.0.1" 
MODBUS_PORT = 502      # Standard Modbus TCP port is 502

# Device Slave ID
SLAVE_ID = 1
# =================================================

def run_gateway():
    print("🔌 Connecting to PostgreSQL Database...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ DB Connection failed: {e}")
        print("Please make sure PostgreSQL is running and credentials are correct.")
        return

    print("🔌 Connecting to Modbus TCP Device...")
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    if not client.connect():
        print(f"❌ Failed to connect to Modbus device at {MODBUS_HOST}:{MODBUS_PORT}")
        return

    print("✅ Gateway is running. Polling every 5 seconds...\n")
    try:
        while True:
            print("-" * 40)
            # ============================================================
            # STEP 1: READ FROM MODBUS & UPDATE 'actuator' TABLE
            # ============================================================
            # Example: Read 2 holding registers starting at address 0
            # Register 0: Current Temperature reading (current_value)
            # Register 1: On/Off Device Status (current_status)
            response = client.read_holding_registers(address=0, count=2, slave=SLAVE_ID)
            
            if not response.isError():
                blower_temp = response.registers[0]
                blower_status = bool(response.registers[1])
                
                print(f"📥 Modbus READ  -> Temp: {blower_temp}°C | Status: {'ON' if blower_status else 'OFF'}")
                
                # Update current state in DB so your Swagger UI / Frontend can see it
                update_query = """
                    UPDATE actuator 
                    SET current_value = %s, current_status = %s, updated_at = NOW() 
                    WHERE name = 'Blower 1';
                """
                # Note: In a real app, you would query by uuid instead of name
                cursor.execute(update_query, (blower_temp, blower_status))
            else:
                print("❌ Error reading from Modbus")

            # ============================================================
            # STEP 2: READ 'blower_config' IN DB & WRITE TO MODBUS
            # ============================================================
            # Example: Retrieve target configuration from DB and send to device
            select_query = """
                SELECT bc.max_temperature 
                FROM blower_config bc
                JOIN actuator a ON bc.actuator_id = a.uuid
                WHERE a.name = 'Blower 1'
            """
            cursor.execute(select_query)
            row = cursor.fetchone()
            
            if row and row[0] is not None:
                max_temp_config = int(row[0])
                
                # We assume the physical PLCs map Modbus Address 2 to "Max Temp"
                # Write this configuration to the physical device.
                client.write_register(address=2, value=max_temp_config, slave=SLAVE_ID)
                
                print(f"📤 Modbus WRITE -> Set Hardware Max Temp to {max_temp_config}°C")

            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Gateway stopped by user.")
    finally:
        client.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_gateway()
