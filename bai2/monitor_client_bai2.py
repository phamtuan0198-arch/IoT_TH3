import asyncio
import datetime
import json
import aiocoap

async def main():
    protocol = await aiocoap.Context.create_client_context()
    uri = "coap://localhost:5683/iot/lab/sensor01/data"
    print("Starting Monitoring CoAP Client... (Nhan Ctrl+C de dung)\n")

    try:
        while True:
            request = aiocoap.Message(code=aiocoap.Code.GET, uri=uri)
            try:
                response = await protocol.request(request).response
                now_str = datetime.datetime.now().strftime("%H:%M:%S")
                data = json.loads(response.payload.decode("utf-8"))

                temp = data.get("temperature", 0)
                hum = data.get("humidity", 0)

                print(f"[{now_str}] Received sensor data")
                print(f"Device: {data.get('device_id')}")
                print(f"Temperature: {temp} C")
                print(f"Humidity: {hum} %")

                has_warning = False
                if temp > 35.0:
                    print("CANH BAO: Nhiet do cao")
                    has_warning = True
                if hum < 40.0:
                    print("CANH BAO: Do am thap")
                    has_warning = True

                if not has_warning:
                    print("Trang thai: Binh thuong")

                print("-" * 30)
            except Exception as e:
                print(f"Loi ket noi den Server: {e}")

            await asyncio.sleep(3)

    except KeyboardInterrupt:
        print("\nDa dung chuong trinh giam sat.")

if __name__ == "__main__":
    asyncio.run(main())