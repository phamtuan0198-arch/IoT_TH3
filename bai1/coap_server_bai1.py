import asyncio
import datetime
import aiocoap
import aiocoap.resource as resource

class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.welcome_message = "Xin chao tu CoAP Server"

    async def render_get(self, request):
        print("GET request received: /iot/lab/message")
        payload = self.welcome_message.encode("utf-8")
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=payload)

    async def render_post(self, request):
        payload_str = request.payload.decode("utf-8")
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        print("POST request received:")
        print(f"Payload: {payload_str}")
        print(f"Time: {now_str}")

        response_payload = "Server da nhan thong diep".encode("utf-8")
        return aiocoap.Message(code=aiocoap.Code.CHANGED, payload=response_payload)

async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "message"], MessageResource())

    await aiocoap.Context.create_server_context(root, bind=("127.0.0.1", 5683))
    print("CoAP Server started on port 5683")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")