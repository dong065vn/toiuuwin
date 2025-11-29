"""
Resources Module - Tài nguyên
Module quản lý tài nguyên và công cụ bổ sung
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class ResourcesModule(BaseModule):
    """Module quản lý tài nguyên - Office Tool, PITVN AVL, Community Resources"""

    def __init__(self, parent):
        super().__init__(parent)
        # Đường dẫn tới các folder tài nguyên
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources = {
            'office_tool': {
                'name': 'Office Tool Plus',
                'path': os.path.join(self.base_path, 'Office_Tool_with_runtime_v10.28.29.0_x64', 'Office Tool'),
                'icon': '📦',
                'description': 'Công cụ quản lý Microsoft Office',
                'exe': 'Office Tool Plus.exe'
            },
            'pitvn_avl': {
                'name': 'PITVN AVL Tool',
                'path': os.path.join(self.base_path, 'PITVN_AVLtool'),
                'icon': '🛠️',
                'description': 'Công cụ kích hoạt Windows & Office',
                'cmd': 'AVL.cmd'
            },
            'pitvn_community': {
                'name': 'PITVN Community Resources',
                'path': os.path.join(self.base_path, 'PITVN Community Resources'),
                'icon': '📚',
                'description': 'Tài nguyên cộng đồng PITVN',
                'file': 'PITVN Community Resources.xlsx'
            }
        }

    def get_module_info(self):
        return {
            'icon': '🎁',
            'name': 'Tài Nguyên',
            'description': 'Công cụ & tài nguyên bổ sung',
            'category': 'resources'
        }

    def create_ui(self):
        """Tạo UI - Resources Management"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🎁 Tài Nguyên - Resources & Tools",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Office Tool Card
        self.create_resource_card(
            content.scrollable_frame,
            self.resources['office_tool'],
            self.open_office_tool
        )

        # PITVN AVL Tool Card
        self.create_resource_card(
            content.scrollable_frame,
            self.resources['pitvn_avl'],
            self.open_pitvn_avl
        )

        # PITVN Community Resources Card
        self.create_resource_card(
            content.scrollable_frame,
            self.resources['pitvn_community'],
            self.open_pitvn_community
        )

        # Quick Actions Card
        quick_card = Card(content.scrollable_frame, title="⚡ Hành động nhanh")
        quick_card.pack(fill='x', pady=(16, 0))

        quick_btns = tk.Frame(quick_card.content_frame, bg=self.colors['bg_card'])
        quick_btns.pack(fill='x', pady=8)

        ModernButton(
            quick_btns, "Mở tất cả thư mục",
            command=self.open_all_folders,
            icon="📂", style='info', width=180, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            quick_btns, "Kiểm tra tài nguyên",
            command=self.check_resources,
            icon="🔍", style='secondary', width=180, height=36
        ).pack(side='left', padx=4)

        # Console
        self.create_console(main)
        self.log("Module Tài Nguyên đã sẵn sàng", "success")
        self.check_resources_silently()

        return main

    def create_resource_card(self, parent, resource, command):
        """Tạo card cho từng tài nguyên"""
        card = Card(parent, title=f"{resource['icon']} {resource['name']}")
        card.pack(fill='x', pady=(0, 16))

        # Description
        desc_frame = tk.Frame(card.content_frame, bg=self.colors['bg_card'])
        desc_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            desc_frame,
            text=resource['description'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            anchor='w'
        ).pack(side='left', fill='x', expand=True)

        # Path
        path_frame = tk.Frame(card.content_frame, bg=self.colors['bg_card'])
        path_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            path_frame,
            text=f"📍 {resource['path']}",
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            font=ModernUI.FONTS['small'],
            anchor='w'
        ).pack(side='left', fill='x', expand=True)

        # Status
        exists = os.path.exists(resource['path'])
        status_text = "✅ Có sẵn" if exists else "❌ Không tìm thấy"
        status_color = self.colors['success'] if exists else self.colors['danger']

        tk.Label(
            path_frame,
            text=status_text,
            bg=self.colors['bg_card'],
            fg=status_color,
            font=ModernUI.FONTS['body_bold']
        ).pack(side='right')

        # Buttons
        btn_frame = tk.Frame(card.content_frame, bg=self.colors['bg_card'])
        btn_frame.pack(fill='x', pady=(8, 0))

        if exists:
            ModernButton(
                btn_frame, "Mở công cụ",
                command=command,
                icon="▶️", style='primary', width=130, height=36
            ).pack(side='left', padx=(0, 8))

        ModernButton(
            btn_frame, "Mở thư mục",
            command=lambda: self.open_folder(resource['path']),
            icon="📂", style='secondary', width=130, height=36
        ).pack(side='left')

    def open_office_tool(self):
        """Mở Office Tool Plus"""
        resource = self.resources['office_tool']
        exe_path = os.path.join(resource['path'], resource['exe'])

        self.log(f"🚀 Đang khởi động {resource['name']}...", "info")

        def run():
            try:
                if os.path.exists(exe_path):
                    subprocess.Popen(exe_path, cwd=resource['path'])
                    self.log(f"✅ Đã mở {resource['name']}!", "success")
                else:
                    self.log(f"❌ Không tìm thấy: {exe_path}", "error")
                    self.show_error("Lỗi", f"Không tìm thấy file:\n{exe_path}")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")
                self.show_error("Lỗi", f"Không thể khởi động:\n{str(e)}")

        threading.Thread(target=run, daemon=True).start()

    def open_pitvn_avl(self):
        """Mở PITVN AVL Tool"""
        resource = self.resources['pitvn_avl']
        cmd_path = os.path.join(resource['path'], resource['cmd'])

        if not self.confirm("Xác nhận",
                           f"Khởi động {resource['name']}?\n\n"
                           "Lưu ý: Công cụ này cần quyền Administrator"):
            return

        self.log(f"🚀 Đang khởi động {resource['name']}...", "info")

        def run():
            try:
                if os.path.exists(cmd_path):
                    # Run CMD and keep window open with /k flag
                    # Use START to run in new window with proper title
                    subprocess.Popen(
                        f'start "PITVN AVL Tool" cmd /k "{cmd_path}"',
                        cwd=resource['path'],
                        shell=True
                    )
                    self.log(f"✅ Đã mở {resource['name']}!", "success")
                else:
                    self.log(f"❌ Không tìm thấy: {cmd_path}", "error")
                    self.show_error("Lỗi", f"Không tìm thấy file:\n{cmd_path}")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")
                self.show_error("Lỗi", f"Không thể khởi động:\n{str(e)}")

        threading.Thread(target=run, daemon=True).start()

    def open_pitvn_community(self):
        """Mở PITVN Community Resources"""
        resource = self.resources['pitvn_community']
        file_path = os.path.join(resource['path'], resource['file'])

        self.log(f"📂 Đang mở {resource['name']}...", "info")

        def run():
            try:
                if os.path.exists(file_path):
                    os.startfile(file_path)
                    self.log(f"✅ Đã mở {resource['name']}!", "success")
                else:
                    self.log(f"❌ Không tìm thấy: {file_path}", "error")
                    self.show_error("Lỗi", f"Không tìm thấy file:\n{file_path}")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")
                self.show_error("Lỗi", f"Không thể mở file:\n{str(e)}")

        threading.Thread(target=run, daemon=True).start()

    def open_folder(self, path):
        """Mở thư mục trong Explorer"""
        self.log(f"📂 Đang mở thư mục: {path}", "info")

        def run():
            try:
                if os.path.exists(path):
                    os.startfile(path)
                    self.log(f"✅ Đã mở thư mục!", "success")
                else:
                    self.log(f"❌ Thư mục không tồn tại!", "error")
                    self.show_error("Lỗi", f"Thư mục không tồn tại:\n{path}")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=run, daemon=True).start()

    def open_all_folders(self):
        """Mở tất cả thư mục tài nguyên"""
        self.log("📂 Đang mở tất cả thư mục tài nguyên...", "info")
        count = 0

        for key, resource in self.resources.items():
            if os.path.exists(resource['path']):
                try:
                    os.startfile(resource['path'])
                    count += 1
                except:
                    pass

        self.log(f"✅ Đã mở {count} thư mục!", "success")

    def check_resources(self):
        """Kiểm tra trạng thái tất cả tài nguyên"""
        self.log("🔍 Đang kiểm tra tài nguyên...\n", "info")

        total = len(self.resources)
        available = 0

        for key, resource in self.resources.items():
            exists = os.path.exists(resource['path'])
            status = "✅ Có sẵn" if exists else "❌ Không tìm thấy"

            self.log(f"{resource['icon']} {resource['name']}: {status}",
                    "success" if exists else "error")
            self.log(f"   Đường dẫn: {resource['path']}\n", "info")

            if exists:
                available += 1

        self.log(f"📊 Tổng kết: {available}/{total} tài nguyên có sẵn",
                "success" if available == total else "warning")

    def check_resources_silently(self):
        """Kiểm tra tài nguyên im lặng (khi khởi động module)"""
        available = sum(1 for r in self.resources.values() if os.path.exists(r['path']))
        total = len(self.resources)

        if available == total:
            self.log(f"✅ Tất cả {total} tài nguyên đều có sẵn", "success")
        else:
            self.log(f"⚠️ Chỉ {available}/{total} tài nguyên có sẵn", "warning")
            self.log("💡 Nhấn 'Kiểm tra tài nguyên' để xem chi tiết", "info")
