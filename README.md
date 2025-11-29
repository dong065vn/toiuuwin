# Windows Optimizer Pro v6.0 - Ultimate Edition

![Version](https://img.shields.io/badge/version-6.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Công cụ tối ưu hóa Windows chuyên nghiệp với giao diện hiện đại, hỗ trợ tiếng Việt đầy đủ.

## Tính năng chính

### 🎯 Quản lý Hệ thống
- Theo dõi hiệu suất CPU, RAM, Disk theo thời gian thực
- Hiển thị thông tin phần cứng chi tiết
- Quản lý các tiến trình đang chạy
- Kiểm tra nhiệt độ và tình trạng hệ thống

### ⚡ Tối ưu hóa
- Tối ưu RAM tự động và theo lịch
- Dọn dẹp Disk với nhiều tùy chọn
- Tối ưu Registry và Prefetch
- Tối ưu hiệu suất hệ thống Windows

### 🚀 Khởi động và Dịch vụ
- Quản lý ứng dụng khởi động cùng Windows
- Quản lý và tối ưu Windows Services
- Tùy chỉnh các tác vụ khởi động

### 🔒 Bảo mật và Riêng tư
- Kiểm tra và tăng cường bảo mật hệ thống
- Quản lý Windows Defender và Firewall
- Tắt các tính năng theo dõi Windows
- Quản lý quyền riêng tư ứng dụng

### 📦 Phần mềm
- Quản lý ứng dụng đã cài đặt
- Gỡ cài đặt hàng loạt
- Tích hợp Office Tool Plus
- Tích hợp PITVN AVL Tools

### 🌐 Mạng
- Tối ưu cài đặt mạng
- Flush DNS và reset network
- Kiểm tra kết nối và tốc độ
- Quản lý network adapters

### 🗂️ File và Thư mục
- Tìm kiếm và xóa file trùng lặp
- Tìm file lớn chiếm dung lượng
- Dọn dẹp file tạm và rác
- Phân tích sử dụng ổ đĩa

### 🏥 Kiểm tra Sức khỏe
- Kiểm tra tình trạng ổ cứng (S.M.A.R.T)
- Kiểm tra lỗi hệ thống (SFC, DISM)
- Kiểm tra Registry
- Báo cáo tổng quan hệ thống

## Giao diện

Windows Optimizer Pro v6.0 có giao diện hiện đại với:
- Dashboard trực quan với card modules
- Hỗ trợ Dark/Light mode
- Thiết kế Material Design
- Hoàn toàn bằng tiếng Việt

## Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11 (64-bit)
- **RAM**: Tối thiểu 4GB
- **Quyền**: Administrator (bắt buộc)
- **Python**: 3.8+ (nếu chạy từ source)

## Cài đặt

### Sử dụng File EXE (Khuyến nghị)

1. Tải file `WindowsOptimizerPro_v6.0.exe` từ thư mục `dist`
2. Right-click file EXE
3. Chọn "Run as Administrator"
4. Cho phép UAC prompt

### Chạy từ Source Code

```bash
# Clone repository
git clone https://github.com/dong065vn/toiuuwin.git
cd toiuuwin

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng với quyền Admin
python app.py
```

## Build từ Source

### Build phiên bản Release (không console)
```bash
python build_app.py
```

### Build phiên bản Debug (có console)
```bash
python build_debug.py
```

File EXE sẽ được tạo trong thư mục `dist/`

## Cấu trúc dự án

```
toiuuwin/
├── app.py                          # Entry point chính
├── build_app.py                    # Script build release
├── build_debug.py                  # Script build debug
├── requirements.txt                # Python dependencies
├── modules/                        # Các module chức năng
│   ├── __init__.py
│   ├── base.py                     # Base module class
│   ├── theme.py                    # Theme manager
│   ├── ui_components.py            # UI components
│   ├── system_module.py            # System monitoring
│   ├── health_module.py            # Health check
│   ├── optimization_module.py      # System optimization
│   ├── startup_module.py           # Startup manager
│   ├── services_module.py          # Services manager
│   ├── privacy_module.py           # Privacy settings
│   ├── software_module.py          # Software manager
│   ├── network_module.py           # Network tools
│   ├── security_module.py          # Security tools
│   ├── files_module.py             # File tools
│   └── resources_module.py         # Resource monitor
├── Office_Tool_with_runtime_v10.28.29.0_x64/  # Office Tool Plus
├── PITVN_AVLtool/                  # PITVN AVL Tools
├── PITVN Community Resources/       # Community resources
└── HUONG_DAN_SU_DUNG.txt           # Hướng dẫn chi tiết

```

## Dependencies

- **tkinter**: GUI framework
- **psutil**: System monitoring
- **wmi**: Windows Management Interface
- **pywin32**: Windows API
- **PyInstaller**: Build tool (dev only)

Xem đầy đủ trong `requirements.txt`

## Tài liệu

- [Hướng dẫn sử dụng chi tiết](HUONG_DAN_SU_DUNG.txt) - Tiếng Việt

## Lưu ý quan trọng

- Ứng dụng **YÊU CẦU** quyền Administrator
- Nên tạo System Restore Point trước khi tối ưu
- Backup dữ liệu quan trọng trước khi thực hiện các thao tác hệ thống
- Một số tính năng có thể yêu cầu khởi động lại máy

## Phát triển

### Thêm module mới

1. Tạo file mới trong `modules/` kế thừa từ `BaseModule`
2. Implement các phương thức bắt buộc: `get_module_info()`, `create_ui()`
3. Import và thêm vào danh sách `module_classes` trong `app.py`

### Coding Style

- Follow PEP 8
- Sử dụng tiếng Việt cho UI strings
- Comments bằng tiếng Việt
- Docstrings bằng tiếng Việt

## Changelog

### v6.0.0 - Ultimate Edition (2024-11)
- Thiết kế lại toàn bộ giao diện với Dashboard
- Chuyển sang kiến trúc module hóa
- Thêm Dark/Light mode
- Tích hợp Office Tool Plus
- Tích hợp PITVN AVL Tools
- Thêm 11 modules chức năng chuyên sâu
- Cải thiện hiệu suất và stability

### v5.0.0 (2024-10)
- Giao diện Material Design
- Thêm System Health Check
- Cải thiện tối ưu RAM
- Thêm Network Tools

### v4.0.0 (2024-09)
- Thêm Privacy Module
- Cải thiện Security Features
- UI/UX improvements

## License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết

## Tác giả

**Windows Optimizer Pro Team**

## Liên hệ & Hỗ trợ

- **GitHub**: [https://github.com/dong065vn/toiuuwin](https://github.com/dong065vn/toiuuwin)
- **Issues**: [https://github.com/dong065vn/toiuuwin/issues](https://github.com/dong065vn/toiuuwin/issues)

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Disclaimer

Phần mềm này được cung cấp "như hiện tại" không có bảo hành. Sử dụng với trách nhiệm của riêng bạn. Tác giả không chịu trách nhiệm cho bất kỳ thiệt hại nào có thể xảy ra.

---

**© 2024 Windows Optimizer Pro Team. All rights reserved.**

Made with ❤️ in Vietnam
