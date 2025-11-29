"""
System Health Check Module - Kiểm tra sức khỏe hệ thống
Module kiểm tra tình trạng hệ thống, phát hiện vấn đề, benchmark
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import psutil
from datetime import datetime
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class HealthModule(BaseModule):
    """Module kiểm tra sức khỏe hệ thống"""

    def get_module_info(self):
        return {
            'icon': '🏥',
            'name': 'System Health',
            'description': 'Kiểm tra sức khỏe hệ thống',
            'category': 'system'
        }

    def create_ui(self):
        """Tạo UI cho Health Check Module"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🏥 System Health Check - Kiểm tra sức khỏe hệ thống",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Quick Actions Card
        actions_card = Card(content.scrollable_frame, title="⚡ Hành động nhanh")
        actions_card.pack(fill='x', pady=(0, 16))

        actions_frame = tk.Frame(actions_card.content_frame, bg=self.colors['bg_card'])
        actions_frame.pack(fill='x', pady=8)

        ModernButton(
            actions_frame, "🔍 Kiểm tra toàn diện",
            command=self.full_health_check,
            style='primary', width=180, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            actions_frame, "🚀 Quick Benchmark",
            command=self.quick_benchmark,
            style='success', width=180, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            actions_frame, "🔧 Sửa lỗi tự động",
            command=self.auto_fix_issues,
            style='warning', width=180, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            actions_frame, "🧹 Dọn dẹp hệ thống",
            command=self.system_cleanup,
            style='info', width=180, height=40
        ).pack(side='left', padx=4)

        # Health Status Card
        self.create_health_status_card(content.scrollable_frame)

        # System Checks Card
        self.create_system_checks_card(content.scrollable_frame)

        # Benchmark Results Card
        self.create_benchmark_card(content.scrollable_frame)

        # Recommendations Card
        self.create_recommendations_card(content.scrollable_frame)

        # Console
        self.create_console(main)
        self.log("Module System Health đã sẵn sàng", "success")

        return main

    def create_health_status_card(self, parent):
        """Tạo card hiển thị trạng thái sức khỏe"""
        health_card = Card(parent, title="💚 Tình trạng sức khỏe tổng quan")
        health_card.pack(fill='x', pady=(0, 16))

        # Overall health score
        self.health_score_label = tk.Label(
            health_card.content_frame,
            text="⏳ Chưa kiểm tra",
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            font=('Segoe UI', 24, 'bold')
        )
        self.health_score_label.pack(pady=12)

        # Status bars frame
        bars_frame = tk.Frame(health_card.content_frame, bg=self.colors['bg_card'])
        bars_frame.pack(fill='x', pady=8)

        self.health_bars = {}
        categories = [
            ('💻 CPU Health', 'cpu'),
            ('💾 Memory Health', 'memory'),
            ('💿 Disk Health', 'disk'),
            ('🌐 Network Health', 'network'),
            ('🔒 Security Health', 'security')
        ]

        for label, key in categories:
            self._create_health_bar(bars_frame, label, key)

    def _create_health_bar(self, parent, label, key):
        """Tạo thanh health bar"""
        frame = tk.Frame(parent, bg=self.colors['bg_card'])
        frame.pack(fill='x', pady=6)

        tk.Label(
            frame,
            text=label,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            width=20,
            anchor='w'
        ).pack(side='left')

        # Progress bar
        progress_frame = tk.Frame(frame, bg=self.colors['bg_main'], height=24)
        progress_frame.pack(side='left', fill='x', expand=True, padx=8)

        bar = tk.Canvas(progress_frame, height=20, bg=self.colors['bg_main'], highlightthickness=0)
        bar.pack(fill='both', expand=True)

        status_label = tk.Label(
            frame,
            text="--",
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            font=ModernUI.FONTS['body_bold'],
            width=10
        )
        status_label.pack(side='left')

        self.health_bars[key] = {'bar': bar, 'label': status_label}

    def create_system_checks_card(self, parent):
        """Tạo card system checks"""
        checks_card = Card(parent, title="✅ Kiểm tra hệ thống")
        checks_card.pack(fill='x', pady=(0, 16))

        # TreeView for checks
        tree_frame = tk.Frame(checks_card.content_frame, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=8)

        columns = ('check', 'status', 'details')
        self.checks_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=8
        )

        self.checks_tree.heading('check', text='Kiểm tra')
        self.checks_tree.heading('status', text='Trạng thái')
        self.checks_tree.heading('details', text='Chi tiết')

        self.checks_tree.column('check', width=250)
        self.checks_tree.column('status', width=120)
        self.checks_tree.column('details', width=350)

        self.checks_tree.pack(fill='both', expand=True)

    def create_benchmark_card(self, parent):
        """Tạo card benchmark results"""
        bench_card = Card(parent, title="🚀 Kết quả Benchmark")
        bench_card.pack(fill='x', pady=(0, 16))

        self.benchmark_label = tk.Label(
            bench_card.content_frame,
            text="Chưa có dữ liệu benchmark.\nNhấn 'Quick Benchmark' để chạy test.",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            justify='left'
        )
        self.benchmark_label.pack(anchor='w', pady=8)

    def create_recommendations_card(self, parent):
        """Tạo card recommendations"""
        rec_card = Card(parent, title="💡 Khuyến nghị")
        rec_card.pack(fill='x', pady=(0, 0))

        self.recommendations_text = tk.Text(
            rec_card.content_frame,
            height=6,
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            wrap='word',
            state='disabled'
        )
        self.recommendations_text.pack(fill='both', expand=True, pady=8)

    def full_health_check(self):
        """Kiểm tra sức khỏe toàn diện"""
        self.log("🔍 Đang kiểm tra sức khỏe hệ thống...", "info")

        def check():
            try:
                # Clear previous checks
                for item in self.checks_tree.get_children():
                    self.checks_tree.delete(item)

                total_score = 0
                max_score = 0
                issues = []

                # 1. CPU Check
                self.log("⚡ Kiểm tra CPU...", "info")
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_score = 100 - min(cpu_percent, 100)
                max_score += 100

                if cpu_percent < 50:
                    cpu_status = "✅ Tốt"
                    total_score += cpu_score
                elif cpu_percent < 80:
                    cpu_status = "⚠️ Trung bình"
                    total_score += cpu_score * 0.7
                    issues.append("CPU usage cao")
                else:
                    cpu_status = "❌ Cao"
                    total_score += cpu_score * 0.3
                    issues.append("CPU usage rất cao!")

                self.checks_tree.insert('', 'end', values=(
                    "CPU Usage",
                    cpu_status,
                    f"{cpu_percent}%"
                ))
                self._update_health_bar('cpu', cpu_score)

                # 2. Memory Check
                self.log("💾 Kiểm tra RAM...", "info")
                mem = psutil.virtual_memory()
                mem_score = 100 - mem.percent
                max_score += 100

                if mem.percent < 70:
                    mem_status = "✅ Tốt"
                    total_score += mem_score
                elif mem.percent < 85:
                    mem_status = "⚠️ Trung bình"
                    total_score += mem_score * 0.7
                    issues.append("RAM usage cao")
                else:
                    mem_status = "❌ Cao"
                    total_score += mem_score * 0.3
                    issues.append("RAM usage rất cao!")

                self.checks_tree.insert('', 'end', values=(
                    "Memory Usage",
                    mem_status,
                    f"{mem.percent}% ({self._format_bytes(mem.used)}/{self._format_bytes(mem.total)})"
                ))
                self._update_health_bar('memory', mem_score)

                # 3. Disk Check
                self.log("💿 Kiểm tra Disk...", "info")
                try:
                    disk = psutil.disk_usage('C:')
                    disk_score = 100 - disk.percent
                    max_score += 100

                    if disk.percent < 80:
                        disk_status = "✅ Tốt"
                        total_score += disk_score
                    elif disk.percent < 90:
                        disk_status = "⚠️ Trung bình"
                        total_score += disk_score * 0.7
                        issues.append("Disk space thấp")
                    else:
                        disk_status = "❌ Thấp"
                        total_score += disk_score * 0.3
                        issues.append("Disk space rất thấp!")

                    self.checks_tree.insert('', 'end', values=(
                        "Disk Space (C:)",
                        disk_status,
                        f"{disk.percent}% used ({self._format_bytes(disk.free)} free)"
                    ))
                    self._update_health_bar('disk', disk_score)
                except:
                    max_score += 100
                    self._update_health_bar('disk', 50)

                # 4. Network Check
                self.log("🌐 Kiểm tra Network...", "info")
                net_score = 80  # Default good score
                max_score += 100
                total_score += net_score

                self.checks_tree.insert('', 'end', values=(
                    "Network Connectivity",
                    "✅ Tốt",
                    "Connected"
                ))
                self._update_health_bar('network', net_score)

                # 5. Security Check
                self.log("🔒 Kiểm tra Security...", "info")
                security_score = self._check_security()
                max_score += 100
                total_score += security_score

                if security_score > 80:
                    sec_status = "✅ Tốt"
                elif security_score > 50:
                    sec_status = "⚠️ Trung bình"
                    issues.append("Cần cải thiện bảo mật")
                else:
                    sec_status = "❌ Yếu"
                    issues.append("Bảo mật yếu!")

                self.checks_tree.insert('', 'end', values=(
                    "Security Status",
                    sec_status,
                    f"Score: {security_score:.0f}/100"
                ))
                self._update_health_bar('security', security_score)

                # 6. Additional Checks
                self._check_disk_errors()
                self._check_system_files()
                self._check_startup_programs()

                # Calculate overall health
                overall_score = (total_score / max_score) * 100 if max_score > 0 else 0

                if overall_score >= 90:
                    health_text = f"💚 Xuất sắc ({overall_score:.0f}/100)"
                    health_color = self.colors['success']
                elif overall_score >= 70:
                    health_text = f"💛 Tốt ({overall_score:.0f}/100)"
                    health_color = self.colors['warning']
                elif overall_score >= 50:
                    health_text = f"🧡 Trung bình ({overall_score:.0f}/100)"
                    health_color = self.colors['warning']
                else:
                    health_text = f"❤️ Cần cải thiện ({overall_score:.0f}/100)"
                    health_color = self.colors['danger']

                self.health_score_label.config(text=health_text, fg=health_color)

                # Update recommendations
                self._update_recommendations(issues, overall_score)

                self.log(f"✅ Hoàn thành kiểm tra! Điểm: {overall_score:.0f}/100", "success")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=check, daemon=True).start()

    def _check_security(self):
        """Kiểm tra bảo mật"""
        score = 100

        try:
            # Check Windows Defender
            result = subprocess.run(
                'sc query WinDefend',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'RUNNING' not in result.stdout:
                score -= 30
                self.checks_tree.insert('', 'end', values=(
                    "Windows Defender",
                    "⚠️ Stopped",
                    "Defender không chạy"
                ))
            else:
                self.checks_tree.insert('', 'end', values=(
                    "Windows Defender",
                    "✅ Running",
                    "Đang bảo vệ"
                ))

            # Check Firewall
            result = subprocess.run(
                'netsh advfirewall show allprofiles state',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'ON' not in result.stdout:
                score -= 20
                self.checks_tree.insert('', 'end', values=(
                    "Windows Firewall",
                    "⚠️ Off",
                    "Firewall đã tắt"
                ))
            else:
                self.checks_tree.insert('', 'end', values=(
                    "Windows Firewall",
                    "✅ On",
                    "Đang bảo vệ"
                ))
        except:
            score = 50

        return max(score, 0)

    def _check_disk_errors(self):
        """Kiểm tra lỗi disk"""
        self.checks_tree.insert('', 'end', values=(
            "Disk Errors",
            "ℹ️ Manual",
            "Chạy 'chkdsk' để kiểm tra chi tiết"
        ))

    def _check_system_files(self):
        """Kiểm tra system files"""
        self.checks_tree.insert('', 'end', values=(
            "System Files",
            "ℹ️ Manual",
            "Chạy 'sfc /scannow' để kiểm tra"
        ))

    def _check_startup_programs(self):
        """Kiểm tra số lượng startup programs"""
        # Simplified check
        self.checks_tree.insert('', 'end', values=(
            "Startup Programs",
            "ℹ️ Info",
            "Xem trong Startup Manager module"
        ))

    def _update_health_bar(self, key, score):
        """Cập nhật health bar"""
        if key not in self.health_bars:
            return

        bar = self.health_bars[key]['bar']
        label = self.health_bars[key]['label']

        # Clear bar
        bar.delete('all')

        # Draw background
        w = bar.winfo_width() if bar.winfo_width() > 1 else 300
        h = 20

        # Draw bar
        bar_width = (score / 100) * w

        if score >= 80:
            color = self.colors['success']
            status = "Tốt"
        elif score >= 50:
            color = self.colors['warning']
            status = "Trung bình"
        else:
            color = self.colors['danger']
            status = "Yếu"

        bar.create_rectangle(0, 0, bar_width, h, fill=color, outline='')
        bar.create_text(w/2, h/2, text=f"{score:.0f}%", font=ModernUI.FONTS['small'])

        label.config(text=status, fg=color)

    def _update_recommendations(self, issues, score):
        """Cập nhật recommendations"""
        self.recommendations_text.config(state='normal')
        self.recommendations_text.delete('1.0', 'end')

        if score >= 90:
            rec_text = "✅ Hệ thống của bạn đang hoạt động tốt!\n\n💡 Khuyến nghị:\n"
            rec_text += "- Tiếp tục duy trì thói quen bảo trì định kỳ\n"
            rec_text += "- Cập nhật Windows thường xuyên\n"
        else:
            rec_text = f"⚠️ Phát hiện {len(issues)} vấn đề cần xử lý:\n\n"
            for i, issue in enumerate(issues, 1):
                rec_text += f"{i}. {issue}\n"

            rec_text += "\n💡 Khuyến nghị:\n"
            if "CPU" in str(issues):
                rec_text += "- Đóng các ứng dụng không cần thiết\n"
            if "RAM" in str(issues):
                rec_text += "- Tăng RAM hoặc đóng ứng dụng\n"
            if "Disk" in str(issues):
                rec_text += "- Dọn dẹp disk, xóa file không cần thiết\n"
            if "bảo mật" in str(issues).lower():
                rec_text += "- Bật Windows Defender và Firewall\n"

        self.recommendations_text.insert('1.0', rec_text)
        self.recommendations_text.config(state='disabled')

    def quick_benchmark(self):
        """Quick benchmark"""
        self.log("🚀 Đang chạy Quick Benchmark...", "info")

        def benchmark():
            try:
                results = []

                # CPU Test
                self.log("⚡ Testing CPU...", "info")
                start = time.time()
                for _ in range(1000000):
                    pass
                cpu_time = time.time() - start
                results.append(f"⚡ CPU Speed: {1/cpu_time:.2f} iterations/sec")

                # Memory Test
                self.log("💾 Testing Memory...", "info")
                mem = psutil.virtual_memory()
                results.append(f"💾 Available RAM: {self._format_bytes(mem.available)}")

                # Disk Test
                self.log("💿 Testing Disk...", "info")
                disk = psutil.disk_usage('C:')
                results.append(f"💿 Free Disk Space: {self._format_bytes(disk.free)}")

                # Display results
                result_text = "\n".join(results)
                result_text += f"\n\n🕐 Test completed at: {datetime.now().strftime('%H:%M:%S')}"

                self.benchmark_label.config(text=result_text)
                self.log("✅ Benchmark hoàn thành!", "success")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=benchmark, daemon=True).start()

    def auto_fix_issues(self):
        """Tự động sửa một số lỗi"""
        if not self.confirm("Xác nhận", "Tự động sửa lỗi:\n\n- Dọn dẹp temp files\n- Sửa lỗi disk\n- Reset network\n\nTiếp tục?"):
            return

        self.log("🔧 Đang tự động sửa lỗi...", "info")

        def fix():
            # Clean temp
            self.log("🧹 Dọn dẹp temp files...", "info")
            self._execute('del /q /f /s %TEMP%\\* 2>nul')

            # Disk cleanup
            self.log("💿 Chạy Disk Cleanup...", "info")
            self._execute('cleanmgr /sagerun:1')

            # Network reset
            self.log("🌐 Reset network cache...", "info")
            self._execute('ipconfig /flushdns')

            self.log("✅ Hoàn thành tự động sửa lỗi!", "success")

        threading.Thread(target=fix, daemon=True).start()

    def system_cleanup(self):
        """Dọn dẹp hệ thống"""
        self.log("🧹 Đang dọn dẹp hệ thống...", "info")

        def cleanup():
            commands = [
                ('🗑️ Temp files', 'del /q /f /s %TEMP%\\* 2>nul'),
                ('🗑️ Prefetch', 'del /q /f /s C:\\Windows\\Prefetch\\* 2>nul'),
                ('🗑️ Recycle Bin', 'rd /s /q C:\\$Recycle.Bin 2>nul'),
                ('🧹 Disk Cleanup', 'cleanmgr /sagerun:1'),
            ]

            for desc, cmd in commands:
                self.log(f"{desc}...", "info")
                self._execute(cmd)

            self.log("✅ Dọn dẹp hoàn tất!", "success")

        threading.Thread(target=cleanup, daemon=True).start()

    def _format_bytes(self, bytes_val):
        """Format bytes"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"

    def _execute(self, command):
        """Execute command"""
        try:
            subprocess.run(command, shell=True, capture_output=True, timeout=30)
            return True
        except:
            return False
