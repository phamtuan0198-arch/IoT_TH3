import asyncio
import json
import aiocoap

async def main():
    protocol = await aiocoap.Context.create_client_context()
    uri = "coap://localhost:5683/iot/lab/light01/status"

    while True:
        cmd = await asyncio.to_thread(input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
        cmd = cmd.strip().upper()

        if cmd == "EXIT":
            print("Thoat chuong trinh điều khiển.")
            break

        elif cmd in ["ON", "OFF"]:
            print("Sending PUT request...")
            payload = json.dumps({"device_id": "light01", "command": cmd}).encode("utf-8")
            request = aiocoap.Message(code=aiocoap.Code.PUT, uri=uri, payload=payload, content_format=50)

            try:
                response = await protocol.request(request).response
                print(f"Response Code: {response.code}")
                if cmd == "ON":
                    print("Da bat den light01\n")
                else:
                    print("Da tat den light01\n")
            except Exception as e:
                print(f"Loi gui lenh PUT: {e}\n")

        elif cmd == "STATUS":
            print("Sending GET request...")
            request = aiocoap.Message(code=aiocoap.Code.GET, uri=uri)
            try:
                response = await protocol.request(request).response
                print("Response:")
                print(response.payload.decode("utf-8") + "\n")
            except Exception as e:
                print(f"Loi gui lenh GET: {e}\n")

        else:
            print("Lenh khong hop le. Vui long nhap ON, OFF, STATUS hoac EXIT.\n")

if __name__ == "__main__":
    asyncio.run(main())