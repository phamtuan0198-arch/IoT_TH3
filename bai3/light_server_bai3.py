import asyncio
import json
import aiocoap
import aiocoap.resource as resource

class SmartLightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.device_id = "light01"
        self.status = "OFF"

    async def render_get(self, request):
        data = {
            "device_id": self.device_id,
            "status": self.status
        }
        payload = json.dumps(data).encode("utf-8")
        return aiocoap.Message(
            code=aiocoap.Code.CONTENT,
            payload=payload,
            content_format=50
        )

    async def render_put(self, request):
        try:
            payload_str = request.payload.decode("utf-8")
            data = json.loads(payload_str)
            command = data.get("command", "").upper()

            if command in ["ON", "OFF"]:
                old_status = self.status
                print(f"\nPUT request received:")
                print(f"Device: {self.device_id}")
                print(f"Command: {command}")

                if old_status != command:
                    self.status = command
                    print(f"Light state changed: {old_status} -> {self.status}")
                    print(f"Notify observers: {self.status}")
                    
                    # Thông báo tới tất cả Observers khi trạng thái thay đổi
                    self.updated_state()

                res_payload = json.dumps({"device_id": self.device_id, "status": self.status}).encode("utf-8")
                return aiocoap.Message(code=aiocoap.Code.CHANGED, payload=res_payload, content_format=50)
            else:
                err_msg = json.dumps({"error": "Command phai la ON hoac OFF"}).encode("utf-8")
                return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=err_msg)

        except Exception as e:
            err_msg = json.dumps({"error": str(e)}).encode("utf-8")
            return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST, payload=err_msg)

async def main():
    root = resource.Site()
    smart_light = SmartLightResource()
    root.add_resource(["iot", "lab", "light01", "status"], smart_light)

    await aiocoap.Context.create_server_context(root, bind=("127.0.0.1", 5683))
    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSmart Light Server stopped.")