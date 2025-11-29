"""
Startup Manager Module - Quản lý chương trình khởi động
Module quản lý các ứng dụng tự động chạy khi Windows khởi động
"""
import tkinter as tk
from tkinter import ttk, messagebox
import winreg
import subprocess
import threading
import os
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class StartupModule(BaseModule):
    """Module quản lý Startup Programs"""

    def get_module_info(self):
        return {
            'icon': '🚀',
            'name': 'Startup Manager',
            'description': 'Quản lý chương trình khởi động',
            'category': 'optimization'
        }

    def create_ui(self):
        """Tạo UI cho Startup Manager"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🚀 Startup Manager - Quản lý chương trình khởi động",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Action buttons
        btn_frame = tk.Frame(header, bg=self.colors['bg_main'])
        btn_frame.pack(side='right')

        ModernButton(
            btn_frame, "Làm mới",
            command=self.load_startup_items,
            icon="🔄", style='primary', width=120, height=36
        ).pack(side='left', padx=5)

        ModernButton(
            btn_frame, "Tắt tất cả",
            command=self.disable_all_startup,
            icon="⛔", style='danger', width=140, height=36
        ).pack(side='left', padx=5)

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Info Card
        info_card = Card(content.scrollable_frame, title="ℹ️ Thông tin")
        info_card.pack(fill='x', pady=(0, 16))

        tk.Label(
            info_card.content_frame,
            text="Quản lý các chương trình tự động chạy khi Windows khởi động.\n"
                 "Tắt các chương trình không cần thiết để cải thiện tốc độ khởi động.",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            justify='left'
        ).pack(anchor='w', pady=4)

        # Startup Items Card
        items_card = Card(content.scrollable_frame, title="📋 Danh sách chương trình khởi động")
        items_card.pack(fill='both', expand=True, pady=(0, 16))

        # Search
        search_frame = tk.Frame(items_card.content_frame, bg=self.colors['bg_card'])
        search_frame.pack(fill='x', pady=(8, 12))

        tk.Label(
            search_frame,
            text="🔍 Tìm kiếm:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=(0, 8))

        self.search_entry = tk.Entry(
            search_frame,
            width=40,
            font=ModernUI.FONTS['body'],
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary']
        )
        self.search_entry.pack(side='left', padx=4)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_startup_items())

        # TreeView
        tree_frame = tk.Frame(items_card.content_frame, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(0, 12))

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')

        # TreeView
        columns = ('name', 'location', 'command', 'status')
        self.startup_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.startup_tree.yview)
        tree_scroll_x.config(command=self.startup_tree.xview)

        # Column headings
        self.startup_tree.heading('name', text='Tên')
        self.startup_tree.heading('location', text='Vị trí')
        self.startup_tree.heading('command', text='Lệnh khởi động')
        self.startup_tree.heading('status', text='Trạng thái')

        # Column widths
        self.startup_tree.column('name', width=200)
        self.startup_tree.column('location', width=150)
        self.startup_tree.column('command', width=350)
        self.startup_tree.column('status', width=100)

        self.startup_tree.pack(fill='both', expand=True)

        # Action buttons
        action_frame = tk.Frame(items_card.content_frame, bg=self.colors['bg_card'])
        action_frame.pack(fill='x', pady=8)

        ModernButton(
            action_frame, "✅ Enable",
            command=self.enable_startup_item,
            style='success', width=120, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "⛔ Disable",
            command=self.disable_startup_item,
            style='warning', width=120, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "🗑️ Delete",
            command=self.delete_startup_item,
            style='danger', width=120, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "📂 Open Location",
            command=self.open_file_location,
            style='info', width=140, height=36
        ).pack(side='left', padx=4)

        # Statistics Card
        stats_card = Card(content.scrollable_frame, title="📊 Thống kê")
        stats_card.pack(fill='x', pady=(0, 0))

        self.stats_label = tk.Label(
            stats_card.content_frame,
            text="",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            justify='left'
        )
        self.stats_label.pack(anchor='w', pady=4)

        # Console
        self.create_console(main)
        self.log("Module Startup Manager đã sẵn sàng", "success")

        # Store startup items
        self.all_startup_items = []

        # Load startup items
        self.load_startup_items()

        return main

    def load_startup_items(self):
        """Load all startup items from registry"""
        self.log("🔄 Đang tải danh sách startup...", "info")

        def load():
            try:
                self.all_startup_items = []

                # Registry locations for startup
                locations = [
                    ("HKCU Run", winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                    ("HKLM Run", winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                    ("HKCU RunOnce", winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                    ("HKLM RunOnce", winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
                    ("HKCU Explorer Run", winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"),
                    ("HKLM Explorer Run", winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"),
                ]

                for loc_name, hkey, path in locations:
                    try:
                        key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                self.all_startup_items.append({
                                    'name': name,
                                    'location': loc_name,
                                    'command': value,
                                    'status': 'Enabled',
                                    'reg_hkey': hkey,
                                    'reg_path': path
                                })
                                i += 1
                            except OSError:
                                break
                        winreg.CloseKey(key)
                    except FileNotFoundError:
                        pass
                    except PermissionError:
                        self.log(f"⚠️ Không có quyền truy cập: {loc_name}", "warning")

                # Also check Startup folder
                self.load_startup_folder_items()

                self.log(f"✅ Đã tải {len(self.all_startup_items)} startup items", "success")
                self.filter_startup_items()
                self.update_statistics()

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=load, daemon=True).start()

    def load_startup_folder_items(self):
        """Load items from Startup folder"""
        startup_folders = [
            (os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup'), "User Startup Folder"),
            (r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup', "Common Startup Folder")
        ]

        for folder, loc_name in startup_folders:
            try:
                if os.path.exists(folder):
                    for item in os.listdir(folder):
                        if item.endswith(('.lnk', '.exe', '.bat', '.cmd')):
                            full_path = os.path.join(folder, item)
                            self.all_startup_items.append({
                                'name': item,
                                'location': loc_name,
                                'command': full_path,
                                'status': 'Enabled',
                                'reg_hkey': None,
                                'reg_path': folder
                            })
            except Exception:
                pass

    def filter_startup_items(self):
        """Filter and display startup items"""
        # Clear tree
        for item in self.startup_tree.get_children():
            self.startup_tree.delete(item)

        search_text = self.search_entry.get().lower()

        # Filter
        filtered = []
        for item in self.all_startup_items:
            if search_text:
                if (search_text not in item['name'].lower() and
                    search_text not in item['command'].lower()):
                    continue
            filtered.append(item)

        # Display
        for item in filtered:
            self.startup_tree.insert('', 'end', values=(
                item['name'],
                item['location'],
                item['command'][:80] + '...' if len(item['command']) > 80 else item['command'],
                item['status']
            ), tags=(item,))

        self.log(f"📊 Hiển thị {len(filtered)}/{len(self.all_startup_items)} startup items", "info")

    def get_selected_item(self):
        """Get selected startup item"""
        selection = self.startup_tree.selection()
        if not selection:
            self.show_error("Lỗi", "Vui lòng chọn một startup item!")
            return None

        item = self.startup_tree.item(selection[0])
        # Find full item data
        for startup_item in self.all_startup_items:
            if (startup_item['name'] == item['values'][0] and
                startup_item['location'] == item['values'][1]):
                return startup_item
        return None

    def enable_startup_item(self):
        """Enable selected startup item"""
        item = self.get_selected_item()
        if not item:
            return

        self.log(f"✅ Enabling: {item['name']}", "info")
        # In real implementation, you would re-add to registry
        messagebox.showinfo("Info", f"Chức năng enable sẽ được thêm trong phiên bản sau.\n\nItem: {item['name']}")

    def disable_startup_item(self):
        """Disable selected startup item"""
        item = self.get_selected_item()
        if not item:
            return

        if not self.confirm("Xác nhận", f"Vô hiệu hóa startup item:\n{item['name']}?"):
            return

        self.log(f"⛔ Disabling: {item['name']}", "warning")

        def disable():
            try:
                if item['reg_hkey'] is not None:
                    # Registry item
                    key = winreg.OpenKey(item['reg_hkey'], item['reg_path'], 0, winreg.KEY_WRITE)
                    winreg.DeleteValue(key, item['name'])
                    winreg.CloseKey(key)
                    self.log(f"✅ Đã vô hiệu hóa: {item['name']}", "success")
                else:
                    # Startup folder item
                    if os.path.exists(item['command']):
                        # Rename with .disabled extension
                        os.rename(item['command'], item['command'] + '.disabled')
                        self.log(f"✅ Đã vô hiệu hóa: {item['name']}", "success")

                self.load_startup_items()

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")
                self.show_error("Lỗi", f"Không thể vô hiệu hóa:\n{str(e)}")

        threading.Thread(target=disable, daemon=True).start()

    def delete_startup_item(self):
        """Delete selected startup item"""
        item = self.get_selected_item()
        if not item:
            return

        if not self.confirm("Cảnh báo", f"XÓA VĨNH VIỄN startup item:\n{item['name']}?\n\nHành động này không thể hoàn tác!"):
            return

        self.disable_startup_item()  # Same as disable for now

    def disable_all_startup(self):
        """Disable all startup items"""
        if not self.confirm("Cảnh báo",
                           "Vô hiệu hóa TẤT CẢ chương trình khởi động?\n\n"
                           "Điều này có thể ảnh hưởng đến các ứng dụng quan trọng!"):
            return

        self.log("⛔ Đang vô hiệu hóa tất cả startup items...", "warning")

        def disable_all():
            count = 0
            for item in self.all_startup_items:
                try:
                    if item['reg_hkey'] is not None:
                        key = winreg.OpenKey(item['reg_hkey'], item['reg_path'], 0, winreg.KEY_WRITE)
                        winreg.DeleteValue(key, item['name'])
                        winreg.CloseKey(key)
                        count += 1
                except:
                    pass

            self.log(f"✅ Đã vô hiệu hóa {count} startup items", "success")
            self.load_startup_items()

        threading.Thread(target=disable_all, daemon=True).start()

    def open_file_location(self):
        """Open file location of selected item"""
        item = self.get_selected_item()
        if not item:
            return

        try:
            # Extract path from command
            command = item['command'].strip('"')
            if os.path.exists(command):
                subprocess.Popen(f'explorer /select,"{command}"')
                self.log(f"📂 Đã mở vị trí file", "success")
            else:
                self.show_error("Lỗi", "Không tìm thấy file!")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def update_statistics(self):
        """Update statistics display"""
        total = len(self.all_startup_items)
        enabled = sum(1 for item in self.all_startup_items if item['status'] == 'Enabled')

        stats_text = f"""
📊 Tổng số: {total} startup items
✅ Enabled: {enabled}
⛔ Disabled: {total - enabled}

💡 Mẹo: Tắt các chương trình không cần thiết để cải thiện tốc độ khởi động Windows.
"""
        self.stats_label.config(text=stats_text.strip())
