# 🚀 Windows Optimizer Pro

Công cụ tối ưu hóa Windows 10/11 chuyên nghiệp với giao diện GUI đẹp mắt và tính năng quản lý cổng mạng (port) mạnh mẽ.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Tính Năng Chính

### 🔧 Tối Ưu Hóa Hệ Thống

- **🗑️ Dọn dẹp file tạm**: Xóa các file tạm thời không cần thiết để giải phóng dung lượng
- **🔒 Tắt Telemetry**: Vô hiệu hóa các dịch vụ thu thập dữ liệu của Windows
- **⚙️ Tối ưu dịch vụ**: Tắt các dịch vụ Windows không cần thiết
- **🚀 Dọn dẹp Prefetch**: Xóa cache prefetch để tăng hiệu suất
- **🎨 Tối ưu hiệu ứng hình ảnh**: Cài đặt hiệu ứng cho hiệu suất tốt nhất
- **🚫 Tối ưu Startup**: Tắt các chương trình khởi động không cần thiết
- **📋 Xóa Event Logs**: Xóa các log sự kiện của Windows
- **🌐 Tối ưu mạng**: Tối ưu cài đặt mạng để có hiệu suất tốt hơn
- **💾 Dọn dẹp ổ đĩa**: Chạy tiện ích dọn dẹp ổ đĩa của Windows
- **⚡ Tối ưu nguồn điện**: Đặt chế độ hiệu suất cao

### 🌐 Quản Lý Cổng Mạng (Port Management)

- **🔍 Quét cổng**: Quét tất cả các cổng đang mở trên hệ thống
- **📊 Hiển thị kết nối**: Xem chi tiết tất cả các kết nối mạng đang hoạt động
- **❌ Đóng tiến trình**: Kết thúc tiến trình đang sử dụng cổng cụ thể
- **🚫 Chặn cổng**: Chặn cổng thông qua Windows Firewall
- **✅ Mở cổng**: Cho phép cổng qua Windows Firewall
- **📈 Thông tin chi tiết**: Hiển thị PID, tên tiến trình, địa chỉ IP, trạng thái kết nối

### 📊 Thông Tin Hệ Thống

- Hiển thị thông tin CPU (số lõi, mức sử dụng)
- Thông tin bộ nhớ RAM (tổng, đã dùng, còn trống)
- Thông tin ổ đĩa (dung lượng, phần trăm sử dụng)
- Thông tin mạng (địa chỉ IP, interface)
- Số lượng tiến trình đang chạy
- Thời gian khởi động hệ thống

## 🎨 Giao Diện

- **Modern Dark Theme**: Giao diện tối hiện đại, dễ nhìn
- **Responsive Design**: Giao diện tự động điều chỉnh
- **Color Coding**: Mã màu cho các trạng thái khác nhau
- **Real-time Updates**: Cập nhật thông tin theo thời gian thực
- **Professional Layout**: Bố cục chuyên nghiệp, dễ sử dụng

## 📋 Yêu Cầu Hệ Thống

- **Hệ điều hành**: Windows 10 hoặc Windows 11
- **Python**: Version 3.7 trở lên
- **Quyền Admin**: Một số tính năng yêu cầu quyền Administrator

## 🔧 Cài Đặt

### Bước 1: Cài đặt Python

Tải và cài đặt Python từ [python.org](https://www.python.org/downloads/)

Đảm bảo chọn "Add Python to PATH" trong quá trình cài đặt.

### Bước 2: Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng

**Chạy bình thường:**
```bash
python win_optimizer.py
```

**Chạy với quyền Administrator (Khuyến nghị):**
- Cách 1: Click chuột phải vào `run_as_admin.bat` và chọn "Run as administrator"
- Cách 2: Mở Command Prompt as Administrator và chạy:
```bash
python win_optimizer.py
```

## 🎯 Hướng Dẫn Sử Dụng

### Tab 1: System Optimization (Tối Ưu Hệ Thống)

1. **Chọn các tùy chọn tối ưu** mà bạn muốn thực hiện
2. Click **"Select All"** để chọn tất cả hoặc tự chọn từng tùy chọn
3. Click **"▶ Run Optimization"** để bắt đầu tối ưu
4. Theo dõi tiến trình trong **Optimization Log**

**⚠️ Lưu ý**: Một số tính năng cần quyền Administrator để hoạt động đầy đủ.

### Tab 2: Port Management (Quản Lý Cổng)

#### Xem kết nối hiện tại:
1. Click **"🔄 Refresh Connections"** để tải danh sách kết nối
2. Xem thông tin chi tiết trong bảng:
   - **PID**: Process ID
   - **Process**: Tên tiến trình
   - **Protocol**: Giao thức (TCP/UDP)
   - **Local Address**: Địa chỉ local
   - **Remote Address**: Địa chỉ từ xa
   - **Status**: Trạng thái kết nối
   - **Port**: Số cổng

#### Quét cổng:
1. Click **"🔍 Scan Ports"** để quét các cổng phổ biến
2. Xem kết quả trong **Port Information**

#### Quản lý tiến trình và cổng:
1. **Chọn một kết nối** trong bảng
2. Chọn hành động:
   - **❌ Kill Selected Process**: Kết thúc tiến trình đang chạy
   - **🚫 Block Port**: Chặn cổng qua Firewall
   - **✅ Allow Port**: Cho phép cổng qua Firewall

**⚠️ Lưu ý**:
- Việc đóng tiến trình hệ thống có thể gây mất ổn định
- Thao tác Firewall cần quyền Administrator

### Tab 3: System Info (Thông Tin Hệ Thống)

- Tự động hiển thị thông tin hệ thống khi mở tab
- Thông tin được cập nhật theo thời gian thực

## 🔒 Bảo Mật

Tool này được thiết kế cho mục đích tối ưu hóa hợp pháp. Các tính năng chặn/mở cổng chỉ nên được sử dụng bởi người dùng có kiến thức về mạng và bảo mật.

**Cảnh báo**:
- ❌ Không chặn các cổng hệ thống quan trọng
- ❌ Không kết thúc các tiến trình hệ thống quan trọng
- ✅ Luôn tạo điểm khôi phục trước khi tối ưu
- ✅ Backup dữ liệu quan trọng

## 📝 Các Lệnh CMD Chuyên Nghiệp Được Sử Dụng

Tool sử dụng các lệnh CMD chuyên nghiệp sau:

### Quản lý dịch vụ:
```cmd
sc stop <service>        # Dừng dịch vụ
sc config <service> start=disabled  # Vô hiệu hóa dịch vụ
```

### Tối ưu mạng:
```cmd
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=enabled
netsh advfirewall firewall add rule ...
```

### Quản lý nguồn:
```cmd
powercfg -setactive <guid>  # Đặt power plan
```

### Dọn dẹp:
```cmd
del /q /f /s %TEMP%\*      # Xóa file tạm
cleanmgr /sagerun:1         # Chạy disk cleanup
```

### Quét thông tin:
```cmd
wmic startup get caption,command  # Lấy danh sách startup
netstat -ano                      # Xem kết nối mạng
```

## 🛠️ Các Thư Viện Sử Dụng

- **tkinter**: Tạo giao diện GUI
- **psutil**: Lấy thông tin hệ thống và quản lý tiến trình
- **subprocess**: Thực thi lệnh CMD
- **socket**: Quét cổng và thông tin mạng
- **threading**: Xử lý đa luồng để không lag GUI

## 🐛 Xử Lý Lỗi

### Lỗi "Access Denied":
- **Nguyên nhân**: Thiếu quyền Administrator
- **Giải pháp**: Chạy ứng dụng với quyền Administrator

### Lỗi "Module not found":
- **Nguyên nhân**: Chưa cài đặt thư viện
- **Giải pháp**: Chạy `pip install -r requirements.txt`

### Lỗi khi tối ưu:
- **Nguyên nhân**: Dịch vụ đang được sử dụng hoặc không tồn tại
- **Giải pháp**: Xem log chi tiết trong Optimization Log

## 🔄 Khôi Phục

Nếu gặp vấn đề sau khi tối ưu:

1. **Khôi phục từ System Restore Point**:
   - Mở System Restore
   - Chọn điểm khôi phục trước khi tối ưu
   - Thực hiện khôi phục

2. **Bật lại dịch vụ đã tắt**:
   ```cmd
   sc config <service_name> start=auto
   sc start <service_name>
   ```

3. **Reset Firewall rules**:
   ```cmd
   netsh advfirewall reset
   ```

## 📊 Hiệu Suất

Sau khi tối ưu, bạn có thể thấy:
- ✅ Giảm thời gian khởi động
- ✅ Tăng tốc độ phản hồi hệ thống
- ✅ Giải phóng RAM
- ✅ Tăng dung lượng ổ đĩa
- ✅ Giảm tải mạng không cần thiết

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Hãy tạo Pull Request hoặc báo lỗi qua Issues.

## 📄 Giấy Phép

Dự án này được phát hành dưới giấy phép MIT License.

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm

Tool này được cung cấp "nguyên trạng" không có bảo hành. Người dùng tự chịu trách nhiệm về việc sử dụng tool. Tác giả không chịu trách nhiệm về bất kỳ thiệt hại nào có thể xảy ra.

## 📞 Liên Hệ & Hỗ Trợ

- **GitHub Issues**: Để báo lỗi và yêu cầu tính năng
- **Discussions**: Để thảo luận và đặt câu hỏi

## 🎓 Mục Đích Giáo Dục

Tool này được tạo ra cho mục đích:
- ✅ Học tập và nghiên cứu
- ✅ Quản trị hệ thống
- ✅ Tối ưu hóa hiệu suất
- ✅ Quản lý mạng

---

**Made with ❤️ for Windows Power Users**

*Phiên bản: 1.0.0*
*Ngày cập nhật: 2025*
