import asyncio
import datetime
import json
import aiocoap

async def main():
    protocol = await aiocoap.Context.create_client_context()
    uri = "coap://localhost:5683/iot/lab/light01/status"

    print("Registering CoAP Observe...")
    request = aiocoap.Message(code=aiocoap.Code.GET, uri=uri, observe=0)
    pr = protocol.request(request)

    # Nhận phản hồi khởi tạo ban đầu
    try:
        first_response = await pr.response
        print("Observe registration successful")
        data = json.loads(first_response.payload.decode("utf-8"))
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        print(f"[{now_str}] Initial State")
        print(f"Device: {data.get('device_id')}")
        print(f"Status: {data.get('status')}\n")
    except Exception as e:
        print(f"Loi dang ky Observe: {e}")
        return

    # Lắng nghe các cập nhật trạng thái tự động từ Server
    try:
        async for response in pr.observation:
            data = json.loads(response.payload.decode("utf-8"))
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now_str}] State Updated")
            print(f"Device: {data.get('device_id')}")
            print(f"Status: {data.get('status')}\n")
    except KeyboardInterrupt:
        print("\nDung giam sat Observe.")

if __name__ == "__main__":
    asyncio.run(main())