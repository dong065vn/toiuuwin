# 🔧 Xử Lý Sự Cố - Windows Optimizer Pro

Hướng dẫn chi tiết để xử lý các vấn đề thường gặp khi cài đặt và sử dụng Windows Optimizer Pro.

## 📦 Vấn Đề Khi Cài Đặt

### ⚠️ "Defaulting to user installation because normal site-packages is not writeable"

**Đây KHÔNG phải là lỗi!** Đây chỉ là cảnh báo thông báo rằng packages đang được cài vào thư mục user thay vì system.

**Nguyên nhân:**
- Bạn đang chạy cài đặt mà không có quyền Administrator
- Windows bảo vệ thư mục system site-packages

**Giải pháp:**

✅ **Không cần làm gì** - Ứng dụng vẫn hoạt động bình thường!

Hoặc nếu muốn cài vào system site-packages:

**Cách 1: Chạy CMD as Administrator**
```batch
# Chuột phải vào Command Prompt
# Chọn "Run as administrator"
pip install -r requirements.txt
```

**Cách 2: Sử dụng --user flag (Khuyến nghị)**
```batch
pip install -r requirements.txt --user
```

**Cách 3: Cài vào Virtual Environment**
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### ⚠️ "Requirement already satisfied"

**Đây cũng KHÔNG phải là lỗi!** Package đã được cài đặt rồi.

**Nguyên nhân:**
- Package psutil đã có trong hệ thống
- Có thể từ lần cài trước hoặc ứng dụng khác

**Giải pháp:**

✅ **Không cần làm gì** - Bạn có thể bắt đầu sử dụng ngay!

Để cập nhật lên phiên bản mới nhất:
```batch
pip install --upgrade psutil
```

---

### ❌ "Python is not installed"

**Giải pháp:**

1. Tải Python từ: https://www.python.org/downloads/
2. **QUAN TRỌNG**: Chọn "Add Python to PATH" khi cài đặt
3. Cài đặt Python 3.7 trở lên (khuyến nghị 3.10+)
4. Khởi động lại Command Prompt
5. Kiểm tra: `python --version`

---

### ❌ "pip is not recognized"

**Giải pháp:**

```batch
# Thử với python -m pip
python -m pip --version

# Nếu vẫn lỗi, cài lại pip
python -m ensurepip --upgrade
```

---

### ❌ "No module named 'tkinter'"

**Nguyên nhân:** tkinter không được cài trong Python

**Giải pháp:**

**Windows:**
- tkinter thường đi kèm Python for Windows
- Cài lại Python và chọn "tcl/tk and IDLE" trong Optional Features

**Linux:**
```bash
sudo apt-get install python3-tk
```

---

### ❌ "ImportError: DLL load failed"

**Nguyên nhân:** Thiếu Visual C++ Redistributable

**Giải pháp:**

Tải và cài đặt Microsoft Visual C++ Redistributable:
https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## 🚀 Vấn Đề Khi Chạy Ứng Dụng

### ❌ "Access Denied" hoặc "Permission Denied"

**Nguyên nhân:** Thiếu quyền Administrator

**Giải pháp:**

1. **Cách 1**: Chuột phải `run_as_admin.bat` → "Run as administrator"
2. **Cách 2**: Mở CMD as Admin → `python win_optimizer.py`
3. **Cách 3**: Tắt UAC tạm thời (không khuyến nghị)

---

### ❌ Ứng dụng không mở hoặc crash ngay

**Kiểm tra:**

```batch
# Chạy với verbose để xem lỗi
python win_optimizer.py
# Xem message lỗi xuất hiện
```

**Các nguyên nhân thường gặp:**

1. **Thiếu psutil:**
```batch
pip install psutil --user
```

2. **Lỗi tkinter:**
```batch
python -c "import tkinter"
# Nếu lỗi, cài lại Python với tcl/tk
```

3. **Python version cũ:**
```batch
python --version
# Cần >= 3.7
```

---

### ❌ "OSError: [WinError 5] Access is denied"

**Nguyên nhân:** Đang cố kill process system hoặc protected

**Giải pháp:**
- Chỉ kill các process của user
- Không kill process của SYSTEM
- Chạy ứng dụng as Administrator

---

### ⚠️ GUI bị lag hoặc đơ

**Nguyên nhân:** Quá nhiều tác vụ chạy cùng lúc

**Giải pháp:**
1. Bỏ chọn một số optimization options
2. Chạy từng tùy chọn một
3. Đợi mỗi tác vụ hoàn thành
4. Đóng các ứng dụng khác

---

### ❌ "FileNotFoundError" khi tối ưu

**Nguyên nhân:** File/folder không tồn tại

**Giải pháp:**
- Bình thường, tool sẽ bỏ qua các file không tồn tại
- Nếu lỗi liên tục, chạy lại ứng dụng
- Kiểm tra log để biết file nào gây lỗi

---

## 🌐 Vấn Đề Port Management

### ❌ "No network connections found"

**Giải pháp:**
1. Click "Refresh Connections" lại
2. Chạy as Administrator
3. Kiểm tra Windows Firewall có block không

---

### ❌ "Cannot kill process"

**Nguyên nhân:**
- Process đang chạy as SYSTEM
- Process được bảo vệ
- Thiếu quyền Administrator

**Giải pháp:**
1. Chạy ứng dụng as Admin
2. Không kill system processes
3. Dùng Task Manager nếu cần thiết

---

### ❌ Firewall rules không hoạt động

**Kiểm tra:**

```batch
# Xem firewall rules
netsh advfirewall firewall show rule name=all

# Xóa rule nếu cần
netsh advfirewall firewall delete rule name="Rule_Name"
```

**Giải pháp:**
1. Chạy ứng dụng as Administrator
2. Kiểm tra Windows Firewall có bật không
3. Kiểm tra antivirus có block không

---

## ⚙️ Vấn Đề Sau Khi Tối Ưu

### ❌ Windows chạy không ổn định

**Giải pháp khôi phục:**

**1. System Restore:**
```
Control Panel → Recovery → Open System Restore
→ Chọn restore point trước khi tối ưu
```

**2. Bật lại services:**
```batch
# Mở CMD as Admin
sc config "ServiceName" start=auto
sc start "ServiceName"
```

**3. Reset network settings:**
```batch
netsh int ip reset
netsh winsock reset
```

**4. Reset firewall:**
```batch
netsh advfirewall reset
```

---

### ❌ Ứng dụng nào đó không chạy

**Nguyên nhân:** Có thể đã disable service cần thiết

**Giải pháp:**

1. Xem log optimization để biết service nào đã disable
2. Bật lại service:

```batch
# Ví dụ: Windows Search
sc config "WSearch" start=auto
sc start "WSearch"
```

**Các service quan trọng KHÔNG nên disable:**
- Wlansvc (WiFi)
- Dhcp (Network)
- DPS (Diagnostic)
- EventLog (quan trọng cho debug)

---

### ❌ Không kết nối được mạng

**Giải pháp:**

```batch
# Reset network
netsh int ip reset
netsh winsock reset
ipconfig /flushdns
ipconfig /renew

# Restart network adapter
netsh interface set interface "Ethernet" admin=disable
netsh interface set interface "Ethernet" admin=enable
```

Sau đó khởi động lại máy.

---

## 🛡️ Vấn Đề Với Antivirus

### ⚠️ Antivirus block ứng dụng

**Nguyên nhân:** Antivirus nhầm tool là malware do:
- Chỉnh sửa registry
- Thay đổi services
- Sử dụng subprocess

**Giải pháp:**

1. **Thêm exception trong Antivirus:**
   - Mở Windows Security
   - Virus & threat protection
   - Manage settings
   - Add or remove exclusions
   - Thêm thư mục chứa tool

2. **Tắt Real-time protection tạm thời** (khi tối ưu)

3. **Whitelist trong Firewall**

---

## 📝 Debug Tips

### Bật debug mode:

**Cách 1: Chạy từ CMD để xem lỗi**
```batch
cd path\to\tool
python win_optimizer.py
# Xem tất cả error messages
```

**Cách 2: Check Event Viewer**
```
Event Viewer → Windows Logs → Application
Tìm errors liên quan đến Python
```

**Cách 3: Test từng module**
```batch
# Test psutil
python -c "import psutil; print(psutil.cpu_percent())"

# Test tkinter
python -c "import tkinter; tkinter.Tk()"

# Test subprocess
python -c "import subprocess; subprocess.run('dir', shell=True)"
```

---

## 🔄 Reset Hoàn Toàn

Nếu mọi thứ đều fail, reset lại:

### 1. Gỡ cài đặt packages:
```batch
pip uninstall psutil -y
```

### 2. Xóa cache:
```batch
rd /s /q %LOCALAPPDATA%\pip\cache
```

### 3. Cài lại:
```batch
pip install -r requirements.txt --user --no-cache-dir
```

### 4. Nếu vẫn không được, dùng Virtual Environment:
```batch
python -m venv fresh_env
fresh_env\Scripts\activate
pip install -r requirements.txt
python win_optimizer.py
```

---

## 📞 Vẫn Gặp Vấn Đề?

### Thông tin cần cung cấp khi báo lỗi:

1. **Python version:**
```batch
python --version
```

2. **OS version:**
```batch
winver
```

3. **Installed packages:**
```batch
pip list
```

4. **Full error message** (chụp màn hình hoặc copy text)

5. **Các bước đã thực hiện**

### Nơi nhận trợ giúp:
- 🐛 GitHub Issues: Báo lỗi chi tiết
- 💬 GitHub Discussions: Đặt câu hỏi
- 📖 README.md: Tài liệu đầy đủ
- 🚀 QUICK_START.md: Hướng dẫn nhanh

---

## 💡 Tips Tránh Lỗi

1. ✅ **Luôn chạy as Administrator** cho full features
2. ✅ **Tạo System Restore Point** trước khi tối ưu
3. ✅ **Backup dữ liệu quan trọng**
4. ✅ **Đọc description** của mỗi optimization option
5. ✅ **Không disable services** mà không hiểu rõ
6. ✅ **Test trên máy ảo** trước nếu không chắc chắn
7. ✅ **Cập nhật Windows** trước khi tối ưu
8. ✅ **Đóng tất cả ứng dụng** trước khi tối ưu

---

**Cập nhật:** 2025-01-12
**Version:** 1.0.0

*Nếu bạn tìm thấy giải pháp cho vấn đề mới, hãy contribute vào file này!*
