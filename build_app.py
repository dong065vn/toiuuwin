"""
Build Script cho Windows Optimizer Pro v6.0
Build app thanh EXE voi PyInstaller
"""
import os
import sys
import subprocess
import shutil

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def build_app():
    """Build ứng dụng thành EXE"""

    print("=" * 80)
    print("WINDOWS OPTIMIZER PRO v6.0 - BUILD SCRIPT")
    print("=" * 80)
    print()

    # Kiểm tra PyInstaller
    print("[1/6] Kiểm tra PyInstaller...")
    try:
        import PyInstaller
        print("✓ PyInstaller đã cài đặt")
    except ImportError:
        print("✗ PyInstaller chưa cài đặt!")
        print("Đang cài đặt PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ Đã cài đặt PyInstaller")

    print()

    # Xóa thư mục build cũ
    print("[2/6] Dọn dẹp build cũ...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Đã xóa {dir_name}/")
            except Exception as e:
                print(f"⚠ Không thể xóa {dir_name}/ (đang sử dụng) - sẽ ghi đè")

    # Xóa file .spec cũ
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        try:
            os.remove(spec_file)
            print(f"✓ Đã xóa {spec_file}")
        except:
            pass

    print()

    # Tạo file manifest cho admin rights
    print("[3/6] Tạo manifest cho quyền Administrator...")
    manifest_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="6.0.0.0"
    processorArchitecture="amd64"
    name="WindowsOptimizerPro"
    type="win32"
  />
  <description>Windows Optimizer Pro v6.0 - Ultimate Edition</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"""

    with open('app.manifest', 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print("✓ Đã tạo app.manifest")

    print()

    # Build với PyInstaller
    print("[4/6] Building với PyInstaller...")
    print("Đang build... (có thể mất 2-5 phút)")
    print()

    build_command = [
        sys.executable,                       # Python executable
        '-m', 'PyInstaller',                  # Run PyInstaller as module
        '--name=WindowsOptimizerPro_v6.0',
        '--onefile',                          # Single EXE file
        '--windowed',                         # No console window
        '--manifest=app.manifest',            # Admin manifest
        '--add-data=modules;modules',         # Include modules folder
        '--add-data=Office_Tool_with_runtime_v10.28.29.0_x64;Office_Tool_with_runtime_v10.28.29.0_x64',
        '--add-data=PITVN_AVLtool;PITVN_AVLtool',
        '--add-data=PITVN Community Resources;PITVN Community Resources',
        '--add-data=requirements.txt;.',
        '--add-data=HUONG_DAN_SU_DUNG.txt;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=psutil',
        '--hidden-import=wmi',
        '--hidden-import=win32com',
        '--hidden-import=win32api',
        '--hidden-import=win32con',
        '--hidden-import=pywintypes',
        '--collect-all=psutil',
        '--collect-all=wmi',
        '--noconsole',                        # Tắt console
        '--clean',                            # Clean cache
        'app.py'
    ]

    try:
        result = subprocess.run(build_command, check=True)
        print("✓ Build thành công!")
    except subprocess.CalledProcessError as e:
        print("✗ Build thất bại!")
        print("Error code:", e.returncode)
        return False
    except Exception as e:
        print("✗ Build thất bại!")
        print("Error:", str(e))
        return False

    print()

    # Copy thêm resources vào dist
    print("[5/6] Copy resources vào dist...")
    dist_path = 'dist'

    # Copy HUONG_DAN_SU_DUNG.txt
    if os.path.exists('HUONG_DAN_SU_DUNG.txt'):
        shutil.copy2('HUONG_DAN_SU_DUNG.txt', dist_path)
        print("✓ Đã copy HUONG_DAN_SU_DUNG.txt")

    # Copy requirements.txt
    if os.path.exists('requirements.txt'):
        shutil.copy2('requirements.txt', dist_path)
        print("✓ Đã copy requirements.txt")

    print()

    # Hoàn thành
    print("[6/6] Hoàn thành!")
    print()
    print("=" * 80)
    print("✓ BUILD THÀNH CÔNG!")
    print("=" * 80)
    print()
    print(f"📂 File EXE: dist\\WindowsOptimizerPro_v6.0.exe")
    print(f"📏 Kích thước: ~{os.path.getsize('dist/WindowsOptimizerPro_v6.0.exe') / (1024*1024):.1f} MB")
    print()
    print("📝 Lưu ý:")
    print("   • EXE yêu cầu quyền Administrator khi chạy")
    print("   • Không có cửa sổ console (windowed mode)")
    print("   • Đã tích hợp đầy đủ 3 folders resources")
    print("   • File hướng dẫn đi kèm trong thư mục dist")
    print()
    print("🚀 Cách chạy:")
    print("   Right-click WindowsOptimizerPro_v6.0.exe → Run as Administrator")
    print()

    # Dọn dẹp
    print("🧹 Dọn dẹp files tạm...")
    if os.path.exists('app.manifest'):
        os.remove('app.manifest')
        print("✓ Đã xóa app.manifest")

    # Tạo file README trong dist
    create_dist_readme()

    print()
    print("=" * 80)

    return True


def create_dist_readme():
    """Tạo file README trong thư mục dist"""
    readme_content = """WINDOWS OPTIMIZER PRO v6.0 - ULTIMATE EDITION
=============================================

CÁCH SỬ DỤNG:
-------------
1. Right-click "WindowsOptimizerPro_v6.0.exe"
2. Chọn "Run as Administrator"
3. Cho phép UAC prompt (Yes)
4. Ứng dụng sẽ khởi động

LƯU Ý:
-------
• Ứng dụng YÊU CẦU quyền Administrator
• Nếu không chạy as Admin, một số tính năng sẽ không hoạt động
• Xem file HUONG_DAN_SU_DUNG.txt để biết cách sử dụng chi tiết

HỖ TRỢ:
-------
Email: support@windowsoptimizer.com
GitHub: https://github.com/windowsoptimizer

© 2024 Windows Optimizer Pro Team
Version 6.0.0 - Ultimate Edition
"""

    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ Đã tạo dist/README.txt")


if __name__ == '__main__':
    try:
        success = build_app()
        if success:
            print("\n✓ BUILD HOÀN TẤT!")
    except KeyboardInterrupt:
        print("\n\n✗ Build bị hủy bởi người dùng")
    except Exception as e:
        print(f"\n\n✗ Lỗi: {str(e)}")
