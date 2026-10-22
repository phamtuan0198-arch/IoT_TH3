import asyncio
import aiocoap

async def main():
    protocol = await aiocoap.Context.create_client_context()
    uri = "coap://localhost:5683/iot/lab/message"

    # 1. Gửi yêu cầu GET
    print("CoAP Client")
    print("Sending GET request...")
    print(f"URI: {uri}")
    
    get_request = aiocoap.Message(code=aiocoap.Code.GET, uri=uri)
    try:
        response = await protocol.request(get_request).response
        print("Response:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8')}\n")
    except Exception as e:
        print(f"Lỗi khi gửi GET: {e}\n")

    # 2. Gửi yêu cầu POST
    print("Sending POST request...")
    post_payload = "Xin chao tu CoAP Client - B23DCCN891 - Pham Anh Tuan"
    print(f"Payload: {post_payload}")

    post_request = aiocoap.Message(
        code=aiocoap.Code.POST,
        uri=uri,
        payload=post_payload.encode("utf-8")
    )
    
    try:
        response = await protocol.request(post_request).response
        print("Response:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"Lỗi khi gửi POST: {e}")

if __name__ == "__main__":
    asyncio.run(main())