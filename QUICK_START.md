# 🚀 Hướng Dẫn Nhanh - Windows Optimizer Pro

## 📦 Cài Đặt Nhanh

### Bước 1: Tải về và giải nén
```bash
# Clone repository hoặc tải về và giải nén
```

### Bước 2: Chạy file cài đặt
```bash
# Double-click vào install.bat
```

### Bước 3: Chạy ứng dụng
```bash
# Double-click vào run_as_admin.bat
```

## 🎯 Sử Dụng Cơ Bản

### 1️⃣ Tối Ưu Hệ Thống Nhanh

1. Mở ứng dụng với quyền Admin
2. Chuyển đến tab **"System Optimization"**
3. Click **"Select All"** để chọn tất cả tùy chọn
4. Click **"▶ Run Optimization"**
5. Đợi quá trình hoàn thành

**⏱️ Thời gian**: Khoảng 2-5 phút

### 2️⃣ Kiểm Tra Cổng Mạng

1. Chuyển đến tab **"Port Management"**
2. Click **"🔄 Refresh Connections"**
3. Xem danh sách các kết nối đang hoạt động

**Mã màu:**
- 🟢 Xanh lá: ESTABLISHED (đang kết nối)
- 🔵 Xanh dương: LISTENING (đang lắng nghe)
- ⚫ Xám: Trạng thái khác

### 3️⃣ Quét Cổng

1. Ở tab **"Port Management"**
2. Click **"🔍 Scan Ports"**
3. Xem kết quả trong **Port Information**

**Các cổng được quét:**
- 21 (FTP)
- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)
- 3389 (RDP)
- Và nhiều cổng phổ biến khác

### 4️⃣ Đóng Tiến Trình Không Mong Muốn

1. Chọn một kết nối trong bảng
2. Click **"❌ Kill Selected Process"**
3. Xác nhận hành động

**⚠️ Cảnh báo**: Không đóng các tiến trình hệ thống!

### 5️⃣ Quản Lý Firewall

**Chặn một cổng:**
1. Chọn kết nối có cổng cần chặn
2. Click **"🚫 Block Port"**
3. Xác nhận

**Mở một cổng:**
1. Chọn kết nối có cổng cần mở
2. Click **"✅ Allow Port"**
3. Xác nhận

## 🔧 Tùy Chọn Tối Ưu Đề Xuất

### Cho Máy Chơi Game:
✅ Clean Temporary Files
✅ Disable Telemetry
✅ Optimize Services
✅ Optimize Visual Effects
✅ Optimize Power Plan
❌ Disable Startup (tự kiểm tra)

### Cho Máy Làm Việc:
✅ Clean Temporary Files
✅ Disable Telemetry
✅ Clean Prefetch
✅ Clear Event Logs
✅ Disk Cleanup
❌ Optimize Visual Effects (nếu cần đồ họa đẹp)

### Cho Máy Yếu:
✅ Tất cả các tùy chọn

## 📊 Kiểm Tra Hiệu Quả

### Trước khi tối ưu:
1. Chuyển đến tab **"System Info"**
2. Ghi lại:
   - CPU Usage
   - RAM Usage
   - Số tiến trình đang chạy

### Sau khi tối ưu:
1. Khởi động lại máy
2. Mở lại ứng dụng
3. Kiểm tra lại các chỉ số
4. So sánh sự khác biệt

**Kết quả mong đợi:**
- ⬇️ Giảm CPU usage 10-20%
- ⬇️ Giảm RAM usage 15-30%
- ⬇️ Giảm số tiến trình 20-40%
- ⚡ Tăng tốc độ khởi động

## ⚠️ Lưu Ý Quan Trọng

### ❗ Trước khi tối ưu:

1. **Tạo System Restore Point:**
   ```
   Tìm kiếm "Create a restore point" trong Windows
   → System Properties
   → Create
   ```

2. **Backup dữ liệu quan trọng**

3. **Đóng tất cả ứng dụng đang chạy**

### ❗ Trong khi tối ưu:

- ⏳ Không tắt máy
- ⏳ Không đóng ứng dụng
- ⏳ Đợi quá trình hoàn thành

### ❗ Sau khi tối ưu:

- 🔄 Khởi động lại máy (khuyến nghị)
- 🔍 Kiểm tra các ứng dụng quan trọng
- 📊 Theo dõi hiệu suất

## 🆘 Xử Lý Sự Cố Nhanh

### Ứng dụng không chạy:
```bash
# Kiểm tra Python
python --version

# Cài đặt lại packages
pip install -r requirements.txt
```

### Thiếu quyền Admin:
- Chuột phải vào `run_as_admin.bat`
- Chọn "Run as administrator"

### Ứng dụng bị lag:
- Giảm số tùy chọn tối ưu chạy cùng lúc
- Chạy từng tùy chọn một

### Lỗi khi tối ưu:
- Xem log chi tiết trong Optimization Log
- Thử chạy lại với quyền Admin
- Tắt antivirus tạm thời

## 🔄 Khôi Phục Nhanh

### Nếu gặp vấn đề:

**Phương pháp 1: System Restore**
```
Control Panel
→ Recovery
→ Open System Restore
→ Chọn restore point trước khi tối ưu
```

**Phương pháp 2: Bật lại dịch vụ**
```cmd
# Mở CMD as Admin
sc config <service_name> start=auto
sc start <service_name>
```

**Phương pháp 3: Reset Firewall**
```cmd
netsh advfirewall reset
```

## 📞 Cần Trợ Giúp?

- 📖 Xem **README.md** để biết chi tiết
- 🐛 Báo lỗi qua GitHub Issues
- 💬 Thảo luận qua GitHub Discussions

## 💡 Mẹo Pro

1. **Chạy định kỳ**: Tối ưu mỗi tuần một lần
2. **Kết hợp với Defrag**: Chạy defrag sau khi tối ưu
3. **Update drivers**: Cập nhật driver thường xuyên
4. **Theo dõi startup**: Kiểm tra startup programs định kỳ
5. **Backup thường xuyên**: Tạo restore point trước mỗi lần tối ưu

## 🎉 Hoàn Thành!

Bạn đã sẵn sàng sử dụng Windows Optimizer Pro!

**Chúc máy tính của bạn chạy nhanh như gió! 🚀**

---
*Phiên bản: 1.0.0*
