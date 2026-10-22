# BÁO CÁO THỰC HÀNH BUỔI 3: LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

---

## 1. Thông tin sinh viên
- **Họ và tên**: Phạm Anh Tuấn
- **Mã sinh viên**: B23DCCN891
- **Lớp**: D23CQCN01-B
- **Môn học**: Lập trình Hệ thống IoT / Mạng máy tính

---

## 2. Phiên bản Python và các thư viện sử dụng
- **Phiên bản Python**: `Python 3.8+` (Khuyến nghị 3.10 hoặc mới hơn)
- **Các thư viện chính**:
  - `aiocoap` (v0.4.x): Thư viện hỗ trợ triển khai CoAP Client, Server và cơ chế CoAP Observe dựa trên `asyncio`.
  - `asyncio`: Thư viện chuẩn quản lý lập trình bất đồng bộ (Asynchronous I/O).
  - `json`: Xử lý định dạng dữ liệu truyền tải (Payload format).
  - `datetime`, `random`, `sys`: Thư viện chuẩn hỗ trợ lấy thời gian, mô phỏng dữ liệu và cấu hình hệ thống.

---

## 3. Cách cài đặt môi trường

### Bước 1: Chuẩn bị Python
Tải và cài đặt Python từ trang chủ [python.org](https://www.python.org/). Khuyến nghị tích hợp Python vào `PATH` của hệ thống.

### Bước 2: Cài đặt thư viện CoAP
Mở Terminal / Command Prompt / PowerShell và chạy lệnh:
```bash
pip install aiocoap
```

### Bước 3: Lưu ý khi chạy trên môi trường Windows
Tránh lỗi `Network error: NetworkError` trên Windows do cơ chế Event Loop mặc định (`ProactorEventLoop`) không tương thích hoàn toàn với UDP socket trong `aiocoap`, bạn cần thêm đoạn mã xử lý ở đầu các file Client:
```python
import sys, asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

---

## 4. Địa chỉ IP, Cổng và URI các tài nguyên CoAP

- **Địa chỉ IP**: `127.0.0.1` (Localhost)
- **Cổng dịch vụ (UDP Port)**: `5683` (Cổng mặc định của CoAP)

### Chi tiết các URI Tài nguyên:

| Bài | Tên tài nguyên | URI CoAP | Các phương thức hỗ trợ | Định dạng Payload |
| :--- | :--- | :--- | :--- | :--- |
| **Bài 1** | Thông điệp cơ bản | `coap://127.0.0.1:5683/iot/lab/message` | `GET`, `POST` | `text/plain` |
| **Bài 2** | Dữ liệu Cảm biến | `coap://127.0.0.1:5683/iot/lab/sensor01/data` | `GET` | `application/json` (50) |
| **Bài 3** | Trạng thái Đèn | `coap://127.0.0.1:5683/iot/lab/light01/status` | `GET`, `PUT`, `Observe` | `application/json` (50) |

---

## 5. Cách chạy từng chương trình

### Cấu trúc thư mục bài tập
```text
THIoT3/
├── bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
├── bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
├── bai3/
│   ├── light_server_bai3.py
│   ├── light_controller_bai3.py
│   └── light_monitor_bai3.py
└── README.md
```

---

### Bài 1: Gửi và nhận thông điệp CoAP cơ bản
1. **Mở Terminal 1 (Khởi động Server):**
   ```bash
   python bai1/coap_server_bai1.py
   ```
2. **Mở Terminal 2 (Khởi động Client):**
   ```bash
   python bai1/coap_client_bai1.py
   ```

---

### Bài 2: Mô phỏng cảm biến Nhiệt độ và Độ ẩm (Polling GET)
1. **Mở Terminal 1 (Khởi động Sensor Server):**
   ```bash
   python bai2/sensor_server_bai2.py
   ```
2. **Mở Terminal 2 (Khởi động Monitoring Client):**
   ```bash
   python bai2/monitor_client_bai2.py
   ```
   *(Nhấn `Ctrl + C` để dừng giám sát)*

---

### Bài 3: Điều khiển và giám sát Đèn thông minh (CoAP Observe)
Cần mở **3 cửa sổ Terminal riêng biệt**:

1. **Terminal 1 (Smart Light Server):**
   ```bash
   python bai3/light_server_bai3.py
   ```
2. **Terminal 2 (Light Monitoring Client - Đăng ký Observe):**
   ```bash
   python bai3/light_monitor_bai3.py
   ```
3. **Terminal 3 (Light Controller Client - Bàn phím điều khiển):**
   ```bash
   python bai3/light_controller_bai3.py
   ```
   *Nhập các lệnh `ON`, `OFF`, `STATUS` để điều khiển và quan sát sự thay đổi trạng thái đẩy về tự động ở Terminal 2.*

---

## 6. Kết quả đạt được của từng bài

### Bài 1
- Xây dựng thành công CoAP Server lắng nghe ở UDP 5683.
- Định nghĩa đúng tài nguyên `/iot/lab/message` hỗ trợ GET và POST.
- CoAP Client thực hiện truy vấn GET nhận câu chào và gửi dữ liệu thông tin sinh viên bằng POST thành công.

### Bài 2
- Mô phỏng cảm biến cập nhật dữ liệu tự động định kỳ 3 giây.
- Phản hồi dữ liệu JSON với `Content-Format: application/json`.
- Monitoring Client lấy dữ liệu bằng cơ chế Polling GET mỗi 3 giây, phân tích JSON và đưa ra cảnh báo chính xác khi `Nhiệt độ > 35°C` hoặc `Độ ẩm < 40%`.

### Bài 3
- Xây dựng tài nguyên dạng `ObservableResource` cho phép theo dõi thay đổi trạng thái theo chuẩn **CoAP Observe (RFC 7641)**.
- Tách biệt luồng điều khiển (PUT) và luồng giám sát thời gian thực (Observe).
- Monitoring Client nhận thông báo đẩy (`Notification`) lập tức ngay khi Controller Client thực hiện lệnh bật/tắt đèn mà không cần vòng lặp Polling GET.

---

## 7. Log minh chứng chương trình hoạt động

### Bài 1: Log chạy thực tế

**Terminal Server (`coap_server_bai1.py`):**
```text
CoAP Server started on port 5683
GET request received: /iot/lab/message
POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN891 - Pham Anh Tuan
Time: 10:15:20
```

**Terminal Client (`coap_client_bai1.py`):**
```text
CoAP Client
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message
Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server

Sending POST request...
Payload: Xin chao tu CoAP Client - B23DCCN891 - Pham Anh Tuan
Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep
```

---

### Bài 2: Log chạy thực tế

**Terminal Server (`sensor_server_bai2.py`):**
```text
Sensor CoAP Server running at coap://localhost:5683/iot/lab/sensor01/data
```

**Terminal Client (`monitor_client_bai2.py`):**
```text
Starting Monitoring CoAP Client... (Nhan Ctrl+C de dung)

[10:20:03] Received sensor data
Device: sensor01
Temperature: 36.1 C
Humidity: 38.7 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
------------------------------
[10:20:06] Received sensor data
Device: sensor01
Temperature: 29.4 C
Humidity: 62.5 %
Trang thai: Binh thuong
------------------------------
```

---

### Bài 3: Log chạy thực tế (3 Terminals)

**Terminal 1: Smart Light Server (`light_server_bai3.py`)**
```text
CoAP Smart Light Server started...
Resource: /iot/lab/light01/status

PUT request received:
Device: light01
Command: ON
Light state changed: OFF -> ON
Notify observers: ON

PUT request received:
Device: light01
Command: OFF
Light state changed: ON -> OFF
Notify observers: OFF
```

**Terminal 2: Monitoring Client (`light_monitor_bai3.py`)**
```text
Registering CoAP Observe...
Observe registration successful
[10:30:00] Initial State
Device: light01
Status: OFF

[10:30:15] State Updated
Device: light01
Status: ON

[10:30:25] State Updated
Device: light01
Status: OFF
```

**Terminal 3: Controller Client (`light_controller_bai3.py`)**
```text
Nhap lenh (ON/OFF/STATUS/EXIT): ON
Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01

Nhap lenh (ON/OFF/STATUS/EXIT): STATUS
Sending GET request...
Response:
{"device_id": "light01", "status": "ON"}

Nhap lenh (ON/OFF/STATUS/EXIT): OFF
Sending PUT request...
Response Code: 2.04 Changed
Da tat den light01
```

---
