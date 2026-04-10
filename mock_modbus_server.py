import asyncio
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

async def run_server():
    print("Initializing Mock Farm Actuator Datastore...")
    # Initialize 100 registers filled with zeros
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100)
    )
    # We set single=True because our SLAVE_ID=1
    context = ModbusServerContext(slaves=store, single=True)
    
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'FarmMock'
    identity.ProductCode = 'FM-1'
    identity.ModelName = 'Mock Farm Actuator'
    identity.MajorMinorRevision = '1.0'
    
    print("Starting Mock Modbus TCP Server on localhost:5020...")
    print("Leave this window open to simulate hardware being powered on.")
    await StartAsyncTcpServer(context=context, identity=identity, address=("127.0.0.1", 5020))

if __name__ == "__main__":
    asyncio.run(run_server())
