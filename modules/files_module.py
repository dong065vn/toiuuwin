"""
Files Module - FULL FEATURES
Module quản lý file và disk cleanup
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import psutil
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class FilesModule(BaseModule):
    """Module quản lý file - Full Features"""

    def get_module_info(self):
        return {
            'icon': '📁',
            'name': 'Tệp tin',
            'description': 'Quản lý tệp tin và dọn dẹp đĩa',
            'category': 'files'
        }

    def create_ui(self):
        """Tạo UI - Full File Operations"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="📁 Quản lý tệp tin",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Cleanup Card
        cleanup_card = Card(content.scrollable_frame, title="🧹 Dọn dẹp hệ thống")
        cleanup_card.pack(fill='x', pady=(0, 16))

        cleanup_btns = tk.Frame(cleanup_card.content_frame, bg=self.colors['bg_card'])
        cleanup_btns.pack(fill='x', pady=8)

        ModernButton(
            cleanup_btns, "Clean Temp Files",
            command=self.clean_temp,
            icon="🗑️", style='warning', width=150, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            cleanup_btns, "Clean Prefetch",
            command=self.clean_prefetch,
            icon="⚡", style='warning', width=140, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            cleanup_btns, "Disk Cleanup",
            command=self.run_disk_cleanup,
            icon="💿", style='primary', width=140, height=36
        ).pack(side='left', padx=4)

        # Analysis Card
        analysis_card = Card(content.scrollable_frame, title="📊 Phân tích đĩa")
        analysis_card.pack(fill='x', pady=(0, 16))

        analysis_btns = tk.Frame(analysis_card.content_frame, bg=self.colors['bg_card'])
        analysis_btns.pack(fill='x', pady=8)

        ModernButton(
            analysis_btns, "Analyze Disk",
            command=self.analyze_disk,
            icon="🔍", style='info', width=130, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            analysis_btns, "Find Large Files",
            command=self.find_large_files,
            icon="📦", style='secondary', width=150, height=36
        ).pack(side='left', padx=4)

        # Browser Cache Card
        browser_card = Card(content.scrollable_frame, title="🌐 Dọn dẹp Browser Cache")
        browser_card.pack(fill='x', pady=(0, 16))

        browser_btns = tk.Frame(browser_card.content_frame, bg=self.colors['bg_card'])
        browser_btns.pack(fill='x', pady=8)

        ModernButton(
            browser_btns, "Clear Chrome Cache",
            command=self.clear_chrome_cache,
            icon="🔵", style='info', width=160, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            browser_btns, "Clear Edge Cache",
            command=self.clear_edge_cache,
            icon="🔷", style='primary', width=150, height=36
        ).pack(side='left', padx=4)

        # Console
        self.create_console(main)
        self.log("Module Tệp tin đã sẵn sàng - Sử dụng các công cụ bên trên", "success")

        return main

    def clean_temp(self):
        """Dọn dẹp temp files"""
        if self.confirm("Xác nhận", "Xóa các file tạm? (Temp files)"):
            self.log("🗑️ Bắt đầu dọn dẹp Temp files...", "info")

            def clean():
                try:
                    # User Temp
                    self.log("Dọn %TEMP%...", "info")
                    result1 = subprocess.run(
                        'rd /s /q %temp%',
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    # Windows Temp
                    self.log("Dọn C:\\Windows\\Temp...", "info")
                    result2 = subprocess.run(
                        'rd /s /q C:\\Windows\\Temp',
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    self.log("✅ Đã dọn dẹp Temp files!", "success")

                except Exception as e:
                    self.log(f"❌ Lỗi: {str(e)}", "error")

            threading.Thread(target=clean, daemon=True).start()

    def clean_prefetch(self):
        """Dọn dẹp Prefetch"""
        if self.confirm("Xác nhận", "Xóa Prefetch files?"):
            self.log("⚡ Bắt đầu dọn dẹp Prefetch...", "info")

            def clean():
                try:
                    result = subprocess.run(
                        'del /f /s /q C:\\Windows\\Prefetch\\*',
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    self.log("✅ Đã dọn dẹp Prefetch!", "success")

                except Exception as e:
                    self.log(f"❌ Lỗi: {str(e)}", "error")

            threading.Thread(target=clean, daemon=True).start()

    def run_disk_cleanup(self):
        """Chạy Windows Disk Cleanup"""
        self.log("💿 Đang mở Disk Cleanup...", "info")
        try:
            subprocess.Popen("cleanmgr", shell=True)
            self.log("✅ Đã mở Disk Cleanup!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def analyze_disk(self):
        """Phân tích sử dụng đĩa"""
        self.log("🔍 Đang phân tích ổ đĩa...", "info")

        def analyze():
            try:
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        self.log(f"\n📀 Ổ: {partition.device}", "info")
                        self.log(f"   Loại: {partition.fstype}", "info")
                        self.log(f"   Tổng: {usage.total / (1024**3):.2f} GB", "info")
                        self.log(f"   Đã dùng: {usage.used / (1024**3):.2f} GB ({usage.percent}%)", "warning")
                        self.log(f"   Còn trống: {usage.free / (1024**3):.2f} GB\n", "success")
                    except:
                        pass

                self.log("✅ Phân tích hoàn tất!", "success")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=analyze, daemon=True).start()

    def find_large_files(self):
        """Tìm files lớn hơn 200MB"""
        self.log("📦 Đang tìm files lớn hơn 200MB...", "info")
        self.log("⏳ Có thể mất vài phút, vui lòng chờ...", "warning")

        def find():
            large_files = []
            limit = 200 * 1024 * 1024  # 200MB
            count = 0

            try:
                for partition in psutil.disk_partitions():
                    if 'removable' not in partition.opts.lower() and 'cdrom' not in partition.opts.lower():
                        try:
                            for root, dirs, files in os.walk(partition.mountpoint):
                                # Skip system folders
                                dirs[:] = [d for d in dirs if d not in ['Windows', 'Program Files', 'Program Files (x86)', '$Recycle.Bin']]

                                for file in files:
                                    try:
                                        filepath = os.path.join(root, file)
                                        size = os.path.getsize(filepath)
                                        if size > limit:
                                            large_files.append((filepath, size))
                                            count += 1
                                            if count % 10 == 0:
                                                self.log(f"Đã tìm thấy {count} files lớn...", "info")
                                    except:
                                        pass
                        except:
                            pass

                self.log(f"\n✅ Tìm thấy {len(large_files)} files lớn hơn 200MB:\n", "success")

                # Sort by size
                large_files.sort(key=lambda x: x[1], reverse=True)

                # Show top 20
                for filepath, size in large_files[:20]:
                    size_mb = size / (1024 * 1024)
                    self.log(f"📦 {size_mb:.2f} MB - {filepath}", "info")

                if len(large_files) > 20:
                    self.log(f"\n... và {len(large_files) - 20} files khác", "info")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=find, daemon=True).start()

    def clear_chrome_cache(self):
        """Xóa Chrome cache"""
        if self.confirm("Xác nhận", "Xóa Chrome cache? (Cần đóng Chrome trước)"):
            self.log("🔵 Đang xóa Chrome cache...", "info")

            def clear():
                try:
                    chrome_cache = os.path.join(
                        os.environ['LOCALAPPDATA'],
                        'Google\\Chrome\\User Data\\Default\\Cache'
                    )

                    if os.path.exists(chrome_cache):
                        subprocess.run(
                            f'rd /s /q "{chrome_cache}"',
                            shell=True,
                            timeout=30
                        )
                        self.log("✅ Đã xóa Chrome cache!", "success")
                    else:
                        self.log("⚠️ Không tìm thấy Chrome cache!", "warning")

                except Exception as e:
                    self.log(f"❌ Lỗi: {str(e)}", "error")

            threading.Thread(target=clear, daemon=True).start()

    def clear_edge_cache(self):
        """Xóa Edge cache"""
        if self.confirm("Xác nhận", "Xóa Edge cache? (Cần đóng Edge trước)"):
            self.log("🔷 Đang xóa Edge cache...", "info")

            def clear():
                try:
                    edge_cache = os.path.join(
                        os.environ['LOCALAPPDATA'],
                        'Microsoft\\Edge\\User Data\\Default\\Cache'
                    )

                    if os.path.exists(edge_cache):
                        subprocess.run(
                            f'rd /s /q "{edge_cache}"',
                            shell=True,
                            timeout=30
                        )
                        self.log("✅ Đã xóa Edge cache!", "success")
                    else:
                        self.log("⚠️ Không tìm thấy Edge cache!", "warning")

                except Exception as e:
                    self.log(f"❌ Lỗi: {str(e)}", "error")

            threading.Thread(target=clear, daemon=True).start()
