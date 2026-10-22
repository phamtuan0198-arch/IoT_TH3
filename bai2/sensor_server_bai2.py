import asyncio
import json
import random
import aiocoap
import aiocoap.resource as resource

class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.device_id = "sensor01"
        self.temperature = round(random.uniform(25.0, 40.0), 1)
        self.humidity = round(random.uniform(30.0, 80.0), 1)
        
        # Tự động cập nhật dữ liệu cảm biến mỗi 3 giây
        asyncio.create_task(self._update_sensor_loop())

    async def _update_sensor_loop(self):
        while True:
            await asyncio.sleep(3)
            self.temperature = round(random.uniform(25.0, 40.0), 1)
            self.humidity = round(random.uniform(30.0, 80.0), 1)

    async def render_get(self, request):
        data = {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        payload = json.dumps(data).encode("utf-8")
        
        # Content-Format 50 đại diện cho application/json trong CoAP
        return aiocoap.Message(
            code=aiocoap.Code.CONTENT,
            payload=payload,
            content_format=50
        )

async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "sensor01", "data"], SensorResource())

    await aiocoap.Context.create_server_context(root, bind=("127.0.0.1", 5683))
    print("Sensor CoAP Server running at coap://localhost:5683/iot/lab/sensor01/data")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor Server stopped.")