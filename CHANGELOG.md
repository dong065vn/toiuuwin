# 📝 Changelog

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại trong file này.

## [2.0.0] - 2025-01-12

### 🎨 Thiết Kế Lại Hoàn Toàn Giao Diện

**Giao Diện Mới:**
- ✅ **Light Theme**: Thay thế dark theme cũ bằng light theme dễ nhìn, không đau mắt
- ✅ **Microsoft Design Language**: Sử dụng color scheme chuyên nghiệp (#0078D4 blue, #F5F6FA background)
- ✅ **Card-based Layout**: Bố cục dạng thẻ hiện đại
- ✅ **Custom ModernButton Class**: Nút bấm tùy chỉnh với hover effects
- ✅ **Scrollable Options**: Panel tùy chọn có thể scroll
- ✅ **Better Spacing**: Padding và spacing được cải thiện

**Color Scheme:**
- Background: #F5F6FA (Light gray - dễ chịu)
- Primary: #0078D4 (Microsoft blue)
- Cards: #FFFFFF (White - sạch đẹp)
- Console: #1E1E1E với text #00FF00
- Success: #107C10, Warning: #FF8C00, Danger: #E81123

### 🌏 Việt Hóa 100%

**Ngôn Ngữ:**
- ✅ Toàn bộ giao diện chuyển sang tiếng Việt
- ✅ Tất cả labels, buttons, headers
- ✅ Tất cả messages và notifications
- ✅ Tất cả log outputs
- ✅ Tooltips và descriptions
- ✅ Error messages

**Thuật Ngữ:**
- Sử dụng thuật ngữ tiếng Việt chuẩn
- Dễ hiểu và phù hợp người Việt

### ✨ Tính Năng Mới (6 Tính Năng!)

- ✅ **🔓 Tắt BitLocker** - Giải mã ổ đĩa (có dialog xác nhận)
- ✅ **💤 Tắt Hibernate** - Vô hiệu hóa ngủ đông để tiết kiệm dung lượng
- ✅ **📁 Xóa Windows.old** - Xóa thư mục cài đặt Windows cũ
- ✅ **🌍 Xóa DNS Cache** - Làm mới bộ nhớ cache DNS
- ✅ **💿 Tối Ưu SSD** - Chạy lệnh TRIM cho SSD
- ✅ **🛡️ Tắt Windows Defender** - Tạm thời (có cảnh báo bảo mật nghiêm ngặt)

### 🔧 Cải Thiện Tính Năng

- ✅ **Nút "Bỏ Chọn Tất Cả"** - Thêm nút để uncheck all options
- ✅ **Better Confirmations** - Dialog xác nhận cho tính năng nguy hiểm
- ✅ **Safety Warnings** - Cảnh báo rõ ràng cho BitLocker và Defender
- ✅ **Realtime Updates** - Console log cập nhật realtime
- ✅ **Thread Safety** - Tối ưu threading để tránh lag

### 📦 Build & Distribution

- ✅ **PyInstaller Support** - Thêm vào requirements.txt
- ✅ **build.bat** - Script tự động build file EXE
- ✅ **BUILD_GUIDE.md** - Hướng dẫn chi tiết build EXE
- ✅ **EXE Ready** - Có thể build thành file exe độc lập

### 📚 Tài Liệu

- ✅ **README.md v2.0** - Viết lại hoàn toàn với thông tin mới
- ✅ **BUILD_GUIDE.md** - Hướng dẫn build EXE chi tiết
- ✅ **Pillow Dependency** - Thêm Pillow cho GUI enhancements

### 🎯 UX Improvements

- ✅ **Header Bar** - Header bar đẹp với title và admin status
- ✅ **Separator Lines** - Visual separators giữa các sections
- ✅ **Color Tags** - Mã màu cho connection status (established, listening)
- ✅ **Better Fonts** - Sử dụng Segoe UI toàn bộ
- ✅ **Hover Effects** - Buttons có hover effect
- ✅ **Cursor Changes** - Cursor thành hand2 khi hover buttons

### 🐛 Bug Fixes

- ✅ Fixed console output encoding
- ✅ Fixed threading issues
- ✅ Improved error handling

---

## [1.0.0] - 2025-01-12

### 🎉 Phiên Bản Đầu Tiên

#### ✨ Tính năng mới

**System Optimization:**
- ✅ Clean Temporary Files - Dọn dẹp file tạm
- ✅ Disable Telemetry - Tắt telemetry
- ✅ Optimize Services - Tối ưu dịch vụ
- ✅ Clean Prefetch - Dọn dẹp prefetch
- ✅ Optimize Visual Effects - Tối ưu hiệu ứng
- ✅ Optimize Startup - Tối ưu startup
- ✅ Clear Event Logs - Xóa event logs
- ✅ Optimize Network - Tối ưu mạng
- ✅ Disk Cleanup - Dọn dẹp ổ đĩa
- ✅ Optimize Power Plan - Tối ưu nguồn

**Port Management:**
- ✅ Quét và hiển thị tất cả kết nối mạng
- ✅ Quét các cổng phổ biến
- ✅ Hiển thị thông tin chi tiết (PID, Process, Protocol, Address, Status)
- ✅ Kết thúc tiến trình theo PID
- ✅ Chặn cổng qua Windows Firewall
- ✅ Mở cổng qua Windows Firewall
- ✅ Mã màu theo trạng thái kết nối

**System Information:**
- ✅ Hiển thị thông tin CPU
- ✅ Hiển thị thông tin RAM
- ✅ Hiển thị thông tin ổ đĩa
- ✅ Hiển thị thông tin mạng
- ✅ Hiển thị số tiến trình
- ✅ Hiển thị thời gian boot

**GUI:**
- ✅ Modern Dark Theme
- ✅ Responsive Design
- ✅ Tab-based Navigation
- ✅ Real-time Logging
- ✅ Color-coded Status
- ✅ Professional Layout

#### 🔧 Cải thiện
- Sử dụng threading để tránh lag GUI
- Kiểm tra quyền Administrator tự động
- Xử lý lỗi toàn diện
- Logging chi tiết cho mọi thao tác

#### 📚 Tài liệu
- README.md đầy đủ
- QUICK_START.md cho người dùng mới
- Hướng dẫn cài đặt chi tiết
- Ví dụ sử dụng

#### 🛠️ Scripts
- install.bat - Script cài đặt tự động
- run_as_admin.bat - Chạy với quyền admin
- requirements.txt - Dependencies

---

## [Upcoming] - Các tính năng sắp tới

### 🎯 Planned Features

**Version 1.1.0:**
- [ ] Schedule optimization - Lên lịch tối ưu tự động
- [ ] Export/Import settings - Xuất/Nhập cài đặt
- [ ] Backup/Restore registry - Sao lưu/Khôi phục registry
- [ ] Custom optimization profiles - Hồ sơ tối ưu tùy chỉnh
- [ ] Performance benchmarking - Đo hiệu suất
- [ ] Dark/Light theme toggle - Chuyển đổi giao diện

**Version 1.2.0:**
- [ ] Advanced port scanning (specific IP ranges)
- [ ] Port monitoring over time
- [ ] Network traffic analysis
- [ ] Firewall rule management interface
- [ ] Process explorer integration

**Version 2.0.0:**
- [ ] Multi-language support
- [ ] Cloud settings sync
- [ ] Plugin system
- [ ] Advanced analytics dashboard
- [ ] Remote management capabilities

### 🐛 Known Issues

Hiện tại không có lỗi được biết đến.

### 💡 Suggestions

Có ý tưởng? Hãy tạo một issue trên GitHub!

---

**Ghi chú:**
- [Added] cho tính năng mới
- [Changed] cho thay đổi trong tính năng hiện có
- [Deprecated] cho tính năng sắp bị loại bỏ
- [Removed] cho tính năng đã bị loại bỏ
- [Fixed] cho bug fixes
- [Security] cho vấn đề bảo mật

