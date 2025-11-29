"""
System Module - FULL FEATURES
Module quản lý thông tin hệ thống, Process Manager và realtime monitoring
"""
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import psutil
import threading
import time
from datetime import datetime
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class SystemModule(BaseModule):
    """Module thông tin hệ thống - Full Features"""

    def get_module_info(self):
        return {
            'icon': '💻',
            'name': 'Hệ thống',
            'description': 'System info, Process Manager, Monitoring',
            'category': 'system'
        }

    def create_ui(self):
        """Tạo UI cho System Module"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="💻 Thông tin hệ thống & Monitoring",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Action buttons
        btn_frame = tk.Frame(header, bg=self.colors['bg_main'])
        btn_frame.pack(side='right')

        ModernButton(
            btn_frame,
            text="Làm mới",
            command=self.refresh_info,
            icon="🔄",
            style='primary',
            width=120
        ).pack(side='left', padx=5)

        # Content area with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Realtime Monitoring Card
        self.create_realtime_card(content.scrollable_frame)

        # Process Manager Card
        self.create_process_manager(content.scrollable_frame)

        # System Info Cards
        self.create_system_info_cards(content.scrollable_frame)

        # Console
        self.create_console(main)
        self.log("Module Hệ thống đã sẵn sàng", "success")

        # Start realtime monitoring
        self.monitoring_active = True
        self.start_monitoring()

        return main

    def create_realtime_card(self, parent):
        """Tạo card monitoring realtime"""
        monitor_card = Card(parent, title="📊 Giám sát thời gian thực")
        monitor_card.pack(fill='x', pady=(0, 16))

        # Create labels for realtime data
        self.rt_labels = {}

        # CPU
        cpu_frame = tk.Frame(monitor_card.content_frame, bg=self.colors['bg_card'])
        cpu_frame.pack(fill='x', pady=4)

        tk.Label(
            cpu_frame,
            text="⚡ CPU:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            width=15,
            anchor='w'
        ).pack(side='left')

        self.rt_labels['cpu'] = tk.Label(
            cpu_frame,
            text="0%",
            bg=self.colors['bg_card'],
            fg=self.colors['primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        )
        self.rt_labels['cpu'].pack(side='left', fill='x', expand=True)

        # Memory
        mem_frame = tk.Frame(monitor_card.content_frame, bg=self.colors['bg_card'])
        mem_frame.pack(fill='x', pady=4)

        tk.Label(
            mem_frame,
            text="💾 RAM:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            width=15,
            anchor='w'
        ).pack(side='left')

        self.rt_labels['mem'] = tk.Label(
            mem_frame,
            text="0%",
            bg=self.colors['bg_card'],
            fg=self.colors['primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        )
        self.rt_labels['mem'].pack(side='left', fill='x', expand=True)

        # Disk
        disk_frame = tk.Frame(monitor_card.content_frame, bg=self.colors['bg_card'])
        disk_frame.pack(fill='x', pady=4)

        tk.Label(
            disk_frame,
            text="💿 Disk C:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            width=15,
            anchor='w'
        ).pack(side='left')

        self.rt_labels['disk'] = tk.Label(
            disk_frame,
            text="0%",
            bg=self.colors['bg_card'],
            fg=self.colors['primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        )
        self.rt_labels['disk'].pack(side='left', fill='x', expand=True)

        # Network
        net_frame = tk.Frame(monitor_card.content_frame, bg=self.colors['bg_card'])
        net_frame.pack(fill='x', pady=4)

        tk.Label(
            net_frame,
            text="🌐 Network:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            width=15,
            anchor='w'
        ).pack(side='left')

        self.rt_labels['net'] = tk.Label(
            net_frame,
            text="↓ 0 KB/s | ↑ 0 KB/s",
            bg=self.colors['bg_card'],
            fg=self.colors['primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        )
        self.rt_labels['net'].pack(side='left', fill='x', expand=True)

        # Process count
        proc_frame = tk.Frame(monitor_card.content_frame, bg=self.colors['bg_card'])
        proc_frame.pack(fill='x', pady=4)

        tk.Label(
            proc_frame,
            text="🔄 Processes:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            width=15,
            anchor='w'
        ).pack(side='left')

        self.rt_labels['procs'] = tk.Label(
            proc_frame,
            text="0",
            bg=self.colors['bg_card'],
            fg=self.colors['primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        )
        self.rt_labels['procs'].pack(side='left', fill='x', expand=True)

    def start_monitoring(self):
        """Start realtime monitoring thread"""
        self.net_io_last = psutil.net_io_counters()

        def monitor():
            while self.monitoring_active:
                try:
                    # CPU
                    cpu_percent = psutil.cpu_percent(interval=0.5)
                    self.rt_labels['cpu'].config(text=f"{cpu_percent}%")

                    # Memory
                    mem = psutil.virtual_memory()
                    self.rt_labels['mem'].config(text=f"{mem.percent}% ({self._format_bytes(mem.used)} / {self._format_bytes(mem.total)})")

                    # Disk C:
                    try:
                        disk = psutil.disk_usage('C:')
                        self.rt_labels['disk'].config(text=f"{disk.percent}% ({self._format_bytes(disk.used)} / {self._format_bytes(disk.total)})")
                    except:
                        pass

                    # Network
                    net_io = psutil.net_io_counters()
                    bytes_sent = net_io.bytes_sent - self.net_io_last.bytes_sent
                    bytes_recv = net_io.bytes_recv - self.net_io_last.bytes_recv
                    self.net_io_last = net_io

                    download_speed = bytes_recv / 1024  # KB/s
                    upload_speed = bytes_sent / 1024  # KB/s
                    self.rt_labels['net'].config(text=f"↓ {download_speed:.1f} KB/s | ↑ {upload_speed:.1f} KB/s")

                    # Process count
                    proc_count = len(psutil.pids())
                    self.rt_labels['procs'].config(text=str(proc_count))

                    time.sleep(1)
                except:
                    pass

        threading.Thread(target=monitor, daemon=True).start()

    def create_process_manager(self, parent):
        """Tạo Process Manager"""
        proc_card = Card(parent, title="🔧 Process Manager")
        proc_card.pack(fill='both', expand=True, pady=(0, 16))

        # Search and refresh
        search_frame = tk.Frame(proc_card.content_frame, bg=self.colors['bg_card'])
        search_frame.pack(fill='x', pady=(8, 12))

        tk.Label(
            search_frame,
            text="🔍 Tìm kiếm:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=(0, 8))

        self.proc_search_entry = tk.Entry(
            search_frame,
            width=30,
            font=ModernUI.FONTS['body'],
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary']
        )
        self.proc_search_entry.pack(side='left', padx=4)
        self.proc_search_entry.bind('<KeyRelease>', lambda e: self.filter_processes())

        ModernButton(
            search_frame, "Làm mới",
            command=self.load_processes,
            icon="🔄", style='primary', width=100, height=32
        ).pack(side='left', padx=8)

        # Sort options
        sort_frame = tk.Frame(proc_card.content_frame, bg=self.colors['bg_card'])
        sort_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            sort_frame,
            text="Sắp xếp:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body']
        ).pack(side='left', padx=(0, 8))

        self.sort_var = tk.StringVar(value='cpu')

        tk.Radiobutton(
            sort_frame,
            text="CPU",
            variable=self.sort_var,
            value='cpu',
            command=self.filter_processes,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=4)

        tk.Radiobutton(
            sort_frame,
            text="Memory",
            variable=self.sort_var,
            value='memory',
            command=self.filter_processes,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=4)

        tk.Radiobutton(
            sort_frame,
            text="Name",
            variable=self.sort_var,
            value='name',
            command=self.filter_processes,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=4)

        # Process TreeView
        tree_frame = tk.Frame(proc_card.content_frame, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(0, 12))

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')

        # TreeView
        columns = ('pid', 'name', 'cpu', 'memory', 'status')
        self.process_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=10,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.process_tree.yview)
        tree_scroll_x.config(command=self.process_tree.xview)

        # Column headings
        self.process_tree.heading('pid', text='PID')
        self.process_tree.heading('name', text='Tên Process')
        self.process_tree.heading('cpu', text='CPU %')
        self.process_tree.heading('memory', text='Memory')
        self.process_tree.heading('status', text='Trạng thái')

        # Column widths
        self.process_tree.column('pid', width=80)
        self.process_tree.column('name', width=250)
        self.process_tree.column('cpu', width=80)
        self.process_tree.column('memory', width=120)
        self.process_tree.column('status', width=100)

        self.process_tree.pack(fill='both', expand=True)

        # Action buttons
        action_frame = tk.Frame(proc_card.content_frame, bg=self.colors['bg_card'])
        action_frame.pack(fill='x', pady=8)

        ModernButton(
            action_frame, "■ End Process",
            command=self.end_process,
            style='danger', width=130, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "⏸️ Suspend",
            command=self.suspend_process,
            style='warning', width=110, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "▶ Resume",
            command=self.resume_process,
            style='success', width=110, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "📊 Details",
            command=self.show_process_details,
            style='info', width=110, height=36
        ).pack(side='left', padx=4)

        # Store all processes for filtering
        self.all_processes = []

        # Load processes
        self.load_processes()

    def load_processes(self):
        """Load all running processes"""
        self.log("🔄 Đang tải danh sách processes...", "info")

        def load():
            try:
                self.all_processes = []

                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
                    try:
                        info = proc.info
                        self.all_processes.append({
                            'pid': info['pid'],
                            'name': info['name'],
                            'cpu': info['cpu_percent'] or 0,
                            'memory': info['memory_info'].rss if info['memory_info'] else 0,
                            'status': info['status']
                        })
                    except:
                        pass

                self.log(f"✅ Đã tải {len(self.all_processes)} processes", "success")
                self.filter_processes()

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=load, daemon=True).start()

    def filter_processes(self):
        """Filter and sort processes"""
        # Clear tree
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        search_text = self.proc_search_entry.get().lower()
        sort_by = self.sort_var.get()

        # Filter
        filtered = []
        for proc in self.all_processes:
            if search_text:
                if search_text not in proc['name'].lower():
                    continue
            filtered.append(proc)

        # Sort
        if sort_by == 'cpu':
            filtered.sort(key=lambda x: x['cpu'], reverse=True)
        elif sort_by == 'memory':
            filtered.sort(key=lambda x: x['memory'], reverse=True)
        elif sort_by == 'name':
            filtered.sort(key=lambda x: x['name'].lower())

        # Display (limit to top 100)
        for proc in filtered[:100]:
            self.process_tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'],
                f"{proc['cpu']:.1f}%",
                self._format_bytes(proc['memory']),
                proc['status']
            ))

        self.log(f"📊 Hiển thị {min(len(filtered), 100)}/{len(filtered)} processes", "info")

    def get_selected_process(self):
        """Get selected process PID"""
        selection = self.process_tree.selection()
        if not selection:
            self.show_error("Lỗi", "Vui lòng chọn một process!")
            return None

        item = self.process_tree.item(selection[0])
        return int(item['values'][0])  # PID

    def end_process(self):
        """End selected process"""
        pid = self.get_selected_process()
        if not pid:
            return

        if not self.confirm("Xác nhận", f"Kết thúc process PID {pid}?"):
            return

        self.log(f"■ Đang kết thúc process PID {pid}...", "info")

        def end():
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=3)
                self.log(f"✅ Đã kết thúc process PID {pid}", "success")
                self.load_processes()
            except psutil.TimeoutExpired:
                proc.kill()
                self.log(f"✅ Đã force kill process PID {pid}", "success")
                self.load_processes()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=end, daemon=True).start()

    def suspend_process(self):
        """Suspend selected process"""
        pid = self.get_selected_process()
        if not pid:
            return

        self.log(f"⏸️ Đang suspend process PID {pid}...", "info")

        def suspend():
            try:
                proc = psutil.Process(pid)
                proc.suspend()
                self.log(f"✅ Đã suspend process PID {pid}", "success")
                self.load_processes()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=suspend, daemon=True).start()

    def resume_process(self):
        """Resume selected process"""
        pid = self.get_selected_process()
        if not pid:
            return

        self.log(f"▶ Đang resume process PID {pid}...", "info")

        def resume():
            try:
                proc = psutil.Process(pid)
                proc.resume()
                self.log(f"✅ Đã resume process PID {pid}", "success")
                self.load_processes()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=resume, daemon=True).start()

    def show_process_details(self):
        """Show process details"""
        pid = self.get_selected_process()
        if not pid:
            return

        try:
            proc = psutil.Process(pid)
            details = f"""
Process Details:

PID: {proc.pid}
Name: {proc.name()}
Status: {proc.status()}
CPU: {proc.cpu_percent()}%
Memory: {self._format_bytes(proc.memory_info().rss)}
Created: {datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')}

Path: {proc.exe() if proc.exe() else 'N/A'}
"""
            messagebox.showinfo("Process Details", details)
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def create_system_info_cards(self, parent):
        """Tạo các card thông tin hệ thống"""
        # OS Information Card
        os_card = Card(parent, title="🖥️ Thông tin hệ điều hành")
        os_card.pack(fill='x', pady=(0, 16))

        os_info = [
            ("Hệ điều hành", platform.system()),
            ("Phiên bản", platform.version()),
            ("Kiến trúc", platform.machine()),
            ("Tên máy tính", platform.node()),
        ]

        for label, value in os_info:
            self._create_info_row(os_card.content_frame, label, value)

        # CPU Information Card
        cpu_card = Card(parent, title="⚡ Thông tin CPU")
        cpu_card.pack(fill='x', pady=(0, 16))

        cpu_info = [
            ("Bộ xử lý", platform.processor()),
            ("Số lõi vật lý", str(psutil.cpu_count(logical=False))),
            ("Số lõi logic", str(psutil.cpu_count(logical=True))),
            ("Tần số", f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "N/A"),
        ]

        for label, value in cpu_info:
            self._create_info_row(cpu_card.content_frame, label, value)

        # Memory Information Card
        mem_card = Card(parent, title="💾 Thông tin bộ nhớ")
        mem_card.pack(fill='x', pady=(0, 16))

        mem = psutil.virtual_memory()
        mem_info = [
            ("Tổng RAM", self._format_bytes(mem.total)),
            ("Đang sử dụng", self._format_bytes(mem.used)),
            ("Khả dụng", self._format_bytes(mem.available)),
            ("Phần trăm sử dụng", f"{mem.percent}%"),
        ]

        for label, value in mem_info:
            self._create_info_row(mem_card.content_frame, label, value)

    def _create_info_row(self, parent, label, value):
        """Tạo một hàng thông tin"""
        row = tk.Frame(parent, bg=self.colors['bg_card'])
        row.pack(fill='x', pady=4)

        tk.Label(
            row,
            text=label + ":",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            width=20,
            anchor='w'
        ).pack(side='left')

        tk.Label(
            row,
            text=value,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold'],
            anchor='w'
        ).pack(side='left', fill='x', expand=True)

    def _format_bytes(self, bytes_val):
        """Format bytes thành đơn vị dễ đọc"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"

    def refresh_info(self):
        """Làm mới thông tin"""
        self.log("Đang làm mới thông tin hệ thống...", "info")
        self.load_processes()
        self.log("Làm mới thành công!", "success")

    def __del__(self):
        """Cleanup when module is destroyed"""
        self.monitoring_active = False
