"""
Optimization Module - FULL FEATURES
Module tối ưu hóa hệ thống Windows với đầy đủ chức năng
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class OptimizationModule(BaseModule):
    """Module tối ưu hóa hệ thống - Full Features"""

    def get_module_info(self):
        return {
            'icon': '⚡',
            'name': 'Tối ưu hóa',
            'description': 'Tối ưu hiệu suất hệ thống Windows',
            'category': 'optimization'
        }

    def create_ui(self):
        """Tạo UI cho Optimization Module"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="⚡ Tối ưu hóa hệ thống Windows",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Restore checkbox at top
        restore_card = Card(content.scrollable_frame, title="↺ Khôi phục")
        restore_card.pack(fill='x', pady=(0, 16))

        self.restore_var = tk.BooleanVar()
        ttk.Checkbutton(
            restore_card.content_frame,
            text="✅ Khôi phục tất cả tính năng đã tắt (Defender, Firewall, Update, SysMain)",
            variable=self.restore_var
        ).pack(anchor='w', pady=4)

        # Optimization options
        self.opt_vars = {}
        self.create_optimization_options(content.scrollable_frame)

        # Action buttons
        btn_frame = tk.Frame(main, bg=self.colors['bg_main'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))

        ModernButton(
            btn_frame,
            text="Bắt đầu tối ưu",
            command=self.apply_optimizations,
            icon="🚀",
            style='primary',
            width=150,
            height=40
        ).pack(side='left', padx=5)

        ModernButton(
            btn_frame,
            text="Khôi phục mặc định",
            command=self.restore_defaults,
            icon="↺",
            style='warning',
            width=150,
            height=40
        ).pack(side='left', padx=5)

        # Console
        self.create_console(main)
        self.log("Module Tối ưu hóa đã sẵn sàng - Chọn tùy chọn và click 'Bắt đầu tối ưu'", "success")

        return main

    def create_optimization_options(self, parent):
        """Tạo các tùy chọn tối ưu hóa - FULL OPTIONS"""

        # ⚡ Power Management
        power_card = Card(parent, title="⚡ Quản lý nguồn")
        power_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['ultimate_perf'] = tk.BooleanVar()
        self.opt_vars['high_perf'] = tk.BooleanVar()
        self.opt_vars['disable_hibernate'] = tk.BooleanVar()
        self.opt_vars['fast_startup'] = tk.BooleanVar()

        ttk.Checkbutton(power_card.content_frame, text="Ultimate Performance Mode",
                       variable=self.opt_vars['ultimate_perf']).pack(anchor='w', pady=2)
        ttk.Checkbutton(power_card.content_frame, text="High Performance Plan",
                       variable=self.opt_vars['high_perf']).pack(anchor='w', pady=2)
        ttk.Checkbutton(power_card.content_frame, text="Tắt Hibernation",
                       variable=self.opt_vars['disable_hibernate']).pack(anchor='w', pady=2)
        ttk.Checkbutton(power_card.content_frame, text="Bật Fast Startup",
                       variable=self.opt_vars['fast_startup']).pack(anchor='w', pady=2)

        # 🎨 Visual Effects
        visual_card = Card(parent, title="🎨 Hiệu ứng đồ họa")
        visual_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['reduce_effects'] = tk.BooleanVar()
        self.opt_vars['disable_aero'] = tk.BooleanVar()
        self.opt_vars['disable_animations'] = tk.BooleanVar()

        ttk.Checkbutton(visual_card.content_frame, text="Giảm Visual Effects",
                       variable=self.opt_vars['reduce_effects']).pack(anchor='w', pady=2)
        ttk.Checkbutton(visual_card.content_frame, text="Tắt Aero Peek",
                       variable=self.opt_vars['disable_aero']).pack(anchor='w', pady=2)
        ttk.Checkbutton(visual_card.content_frame, text="Tắt Animations",
                       variable=self.opt_vars['disable_animations']).pack(anchor='w', pady=2)

        # 🔍 Search & Indexing
        search_card = Card(parent, title="🔍 Search & Indexing")
        search_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['disable_search'] = tk.BooleanVar()
        self.opt_vars['disable_sysmain'] = tk.BooleanVar()

        ttk.Checkbutton(search_card.content_frame, text="Giảm Windows Search",
                       variable=self.opt_vars['disable_search']).pack(anchor='w', pady=2)
        ttk.Checkbutton(search_card.content_frame, text="Tắt SysMain (SuperFetch)",
                       variable=self.opt_vars['disable_sysmain']).pack(anchor='w', pady=2)

        # 🌟 Windows Features
        features_card = Card(parent, title="🌟 Tính năng Windows")
        features_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['disable_spotlight'] = tk.BooleanVar()
        self.opt_vars['disable_bg_apps'] = tk.BooleanVar()
        self.opt_vars['disable_clipboard'] = tk.BooleanVar()
        self.opt_vars['disable_focus_assist'] = tk.BooleanVar()

        ttk.Checkbutton(features_card.content_frame, text="Tắt Spotlight",
                       variable=self.opt_vars['disable_spotlight']).pack(anchor='w', pady=2)
        ttk.Checkbutton(features_card.content_frame, text="Tắt Background Apps",
                       variable=self.opt_vars['disable_bg_apps']).pack(anchor='w', pady=2)
        ttk.Checkbutton(features_card.content_frame, text="Tắt Clipboard History",
                       variable=self.opt_vars['disable_clipboard']).pack(anchor='w', pady=2)
        ttk.Checkbutton(features_card.content_frame, text="Tắt Focus Assist",
                       variable=self.opt_vars['disable_focus_assist']).pack(anchor='w', pady=2)

        # 🎮 Gaming & Performance
        gaming_card = Card(parent, title="🎮 Gaming & Performance")
        gaming_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['enable_game_mode'] = tk.BooleanVar()
        self.opt_vars['enable_gpu_scheduling'] = tk.BooleanVar()
        self.opt_vars['optimize_memory'] = tk.BooleanVar()

        ttk.Checkbutton(gaming_card.content_frame, text="✅ Bật Game Mode",
                       variable=self.opt_vars['enable_game_mode']).pack(anchor='w', pady=2)
        ttk.Checkbutton(gaming_card.content_frame, text="✅ Bật GPU Hardware Scheduling",
                       variable=self.opt_vars['enable_gpu_scheduling']).pack(anchor='w', pady=2)
        ttk.Checkbutton(gaming_card.content_frame, text="✅ Tối ưu Memory Compression",
                       variable=self.opt_vars['optimize_memory']).pack(anchor='w', pady=2)

        # 💾 Storage Optimization
        storage_card = Card(parent, title="💾 Storage Optimization")
        storage_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['enable_storage_sense'] = tk.BooleanVar()
        self.opt_vars['disable_last_access'] = tk.BooleanVar()
        self.opt_vars['optimize_ntfs'] = tk.BooleanVar()
        self.opt_vars['ssd_optimize'] = tk.BooleanVar()
        self.opt_vars['trim_enable'] = tk.BooleanVar()

        ttk.Checkbutton(storage_card.content_frame, text="✅ Bật Storage Sense (Auto Cleanup)",
                       variable=self.opt_vars['enable_storage_sense']).pack(anchor='w', pady=2)
        ttk.Checkbutton(storage_card.content_frame, text="✅ Tắt NTFS Last Access Time",
                       variable=self.opt_vars['disable_last_access']).pack(anchor='w', pady=2)
        ttk.Checkbutton(storage_card.content_frame, text="✅ Optimize MFT Zone",
                       variable=self.opt_vars['optimize_ntfs']).pack(anchor='w', pady=2)
        ttk.Checkbutton(storage_card.content_frame, text="💿 Tối ưu SSD (Disable Prefetch, Superfetch)",
                       variable=self.opt_vars['ssd_optimize']).pack(anchor='w', pady=2)
        ttk.Checkbutton(storage_card.content_frame, text="💿 Bật TRIM cho SSD",
                       variable=self.opt_vars['trim_enable']).pack(anchor='w', pady=2)

        # 🔄 Windows Update
        update_card = Card(parent, title="🔄 Windows Update")
        update_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['disable_update'] = tk.BooleanVar()
        self.opt_vars['clear_update_cache'] = tk.BooleanVar()

        ttk.Checkbutton(update_card.content_frame, text="⚠️ Tắt Windows Update",
                       variable=self.opt_vars['disable_update']).pack(anchor='w', pady=2)
        ttk.Checkbutton(update_card.content_frame, text="Xóa Update Cache",
                       variable=self.opt_vars['clear_update_cache']).pack(anchor='w', pady=2)

        # 🛡️ Security (with warnings)
        security_card = Card(parent, title="🛡️ Bảo mật (CẨN THẬN!)")
        security_card.pack(fill='x', pady=(0, 12))

        self.opt_vars['disable_defender'] = tk.BooleanVar()
        self.opt_vars['disable_firewall'] = tk.BooleanVar()
        self.opt_vars['disable_bitlocker'] = tk.BooleanVar()

        ttk.Checkbutton(security_card.content_frame, text="⚠️ Tắt Windows Defender (RỦI RO CAO!)",
                       variable=self.opt_vars['disable_defender']).pack(anchor='w', pady=2)
        ttk.Checkbutton(security_card.content_frame, text="⚠️ Tắt Windows Firewall (RỦI RO CAO!)",
                       variable=self.opt_vars['disable_firewall']).pack(anchor='w', pady=2)
        ttk.Checkbutton(security_card.content_frame, text="⚠️ Tắt BitLocker (RỦI RO CAO!)",
                       variable=self.opt_vars['disable_bitlocker']).pack(anchor='w', pady=2)

        tk.Label(
            security_card.content_frame,
            text="⚠️ CHỈ tắt nếu bạn có giải pháp thay thế!",
            font=ModernUI.FONTS['small'],
            fg=self.colors['danger'],
            bg=self.colors['bg_card']
        ).pack(anchor='w', pady=4)

    def apply_optimizations(self):
        """Áp dụng các tối ưu hóa - FULL IMPLEMENTATION"""

        # Check restore mode first
        if self.restore_var.get():
            self.restore_features()
            return

        # Check for dangerous options
        if (self.opt_vars['disable_defender'].get() or
            self.opt_vars['disable_firewall'].get() or
            self.opt_vars['disable_bitlocker'].get()):

            if not messagebox.askyesno(
                "Cảnh báo Bảo mật",
                "Bạn đang TẮT tính năng bảo mật quan trọng!\n\n"
                "Điều này có thể khiến máy tính dễ bị tấn công.\n"
                "BitLocker sẽ decrypt dữ liệu và làm mất bảo mật!\n\n"
                "Bạn có chắc chắn muốn tiếp tục?"
            ):
                return

        self.log("🚀 Bắt đầu quá trình tối ưu hóa...", "info")

        def run_optimizations():
            count = 0

            # ⚡ Power Management
            if self.opt_vars['ultimate_perf'].get():
                self.log("⚡ Bật Ultimate Performance Mode...", "info")
                self._execute('powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61')
                count += 1

            if self.opt_vars['high_perf'].get():
                self.log("⚡ Chuyển sang High Performance...", "info")
                self._execute('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
                count += 1

            if self.opt_vars['disable_hibernate'].get():
                self.log("💤 Tắt Hibernation...", "info")
                self._execute('powercfg /hibernate off')
                count += 1

            if self.opt_vars['fast_startup'].get():
                self.log("⚡ Bật Fast Startup...", "info")
                self._execute('powercfg /hibernate on')
                self._execute('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d 1 /f')
                count += 1

            # 🎨 Visual Effects
            if self.opt_vars['reduce_effects'].get():
                self.log("🎨 Giảm Visual Effects...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f')
                count += 1

            if self.opt_vars['disable_aero'].get():
                self.log("🎨 Tắt Aero Peek...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\DWM" /v EnableAeroPeek /t REG_DWORD /d 0 /f')
                count += 1

            if self.opt_vars['disable_animations'].get():
                self.log("🎨 Tắt Animations...", "info")
                self._execute('reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f')
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v TaskbarAnimations /t REG_DWORD /d 0 /f')
                count += 1

            # 🔍 Search & Indexing
            if self.opt_vars['disable_search'].get():
                self.log("🔍 Giảm Windows Search...", "info")
                self._execute('sc config "WSearch" start=demand')
                count += 1

            if self.opt_vars['disable_sysmain'].get():
                self.log("🔍 Tắt SysMain (SuperFetch)...", "info")
                self._execute('sc stop "SysMain"')
                self._execute('sc config "SysMain" start=disabled')
                count += 1

            # 🌟 Windows Features
            if self.opt_vars['disable_spotlight'].get():
                self.log("🌟 Tắt Spotlight...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-338389Enabled /t REG_DWORD /d 0 /f')
                count += 1

            if self.opt_vars['disable_bg_apps'].get():
                self.log("🌟 Tắt Background Apps...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f')
                self._execute('reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\AppPrivacy" /v LetAppsRunInBackground /t REG_DWORD /d 2 /f')
                count += 1

            if self.opt_vars['disable_clipboard'].get():
                self.log("🌟 Tắt Clipboard History...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 0 /f')
                count += 1

            if self.opt_vars['disable_focus_assist'].get():
                self.log("🌟 Tắt Focus Assist...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\Cache\\DefaultAccount" /v Data /t REG_BINARY /d 0 /f')
                count += 1

            # 🎮 Gaming & Performance
            if self.opt_vars['enable_game_mode'].get():
                self.log("🎮 Bật Game Mode...", "success")
                self._execute('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f')
                self._execute('reg add "HKCU\\Software\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f')
                count += 1

            if self.opt_vars['enable_gpu_scheduling'].get():
                self.log("🎮 Bật Hardware-Accelerated GPU Scheduling...", "success")
                self._execute('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f')
                count += 1

            if self.opt_vars['optimize_memory'].get():
                self.log("🎮 Tối ưu Memory Compression...", "success")
                self._execute('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v DisablePagingExecutive /t REG_DWORD /d 1 /f')
                count += 1

            # 💾 Storage Optimization
            if self.opt_vars['enable_storage_sense'].get():
                self.log("💾 Bật Storage Sense...", "success")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v 01 /t REG_DWORD /d 1 /f')
                count += 1

            if self.opt_vars['disable_last_access'].get():
                self.log("💾 Tắt NTFS Last Access Time...", "success")
                self._execute('fsutil behavior set disablelastaccess 1')
                count += 1

            if self.opt_vars['optimize_ntfs'].get():
                self.log("💾 Optimize NTFS MFT Zone...", "success")
                self._execute('fsutil behavior set mftzone 2')
                count += 1

            if self.opt_vars['ssd_optimize'].get():
                self.log("💿 Tối ưu cho SSD...", "success")
                self._execute('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')
                self._execute('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 0 /f')
                count += 1

            if self.opt_vars['trim_enable'].get():
                self.log("💿 Bật TRIM cho SSD...", "success")
                self._execute('fsutil behavior set DisableDeleteNotify 0')
                count += 1

            # 🔄 Windows Update
            if self.opt_vars['disable_update'].get():
                self.log("🔄 Tắt Windows Update...", "warning")
                self._execute('sc stop "wuauserv"')
                self._execute('sc config "wuauserv" start=disabled')
                count += 1

            if self.opt_vars['clear_update_cache'].get():
                self.log("🔄 Xóa Update Cache...", "info")
                self._execute('rd /s /q C:\\Windows\\SoftwareDistribution\\Download')
                count += 1

            # 🛡️ Security (Dangerous!)
            if self.opt_vars['disable_defender'].get():
                self.log("⚠️ TẮT Windows Defender...", "error")
                self._execute('powershell Set-MpPreference -DisableRealtimeMonitoring $true')
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f')
                count += 1

            if self.opt_vars['disable_firewall'].get():
                self.log("⚠️ TẮT Windows Firewall...", "error")
                self._execute('netsh advfirewall set allprofiles state off')
                count += 1

            if self.opt_vars['disable_bitlocker'].get():
                self.log("⚠️ TẮT BitLocker...", "error")
                self._execute('manage-bde -off C:')
                count += 1

            self.log(f"✅ Hoàn thành! Đã áp dụng {count} tối ưu hóa.", "success")
            self.log("ℹ️ Một số thay đổi cần khởi động lại máy để có hiệu lực.", "info")

        threading.Thread(target=run_optimizations, daemon=True).start()

    def restore_features(self):
        """Khôi phục các tính năng đã tắt"""
        self.log("↺ Chế độ khôi phục - Bật lại các tính năng...", "warning")

        def run_restore():
            self.log("🛡️ Bật Windows Defender...", "info")
            self._execute('reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /f')

            self.log("🛡️ Bật Windows Firewall...", "info")
            self._execute('netsh advfirewall set allprofiles state on')

            self.log("🔄 Bật Windows Update...", "info")
            self._execute('sc config "wuauserv" start=auto')
            self._execute('sc start "wuauserv"')

            self.log("🔍 Bật SysMain...", "info")
            self._execute('sc config "SysMain" start=auto')
            self._execute('sc start "SysMain"')

            self.log("✅ Hoàn thành khôi phục!", "success")

        threading.Thread(target=run_restore, daemon=True).start()

    def restore_defaults(self):
        """Khôi phục cài đặt power mặc định"""
        if self.confirm("Khôi phục", "Khôi phục power plan mặc định?"):
            self.log("↺ Khôi phục power plans...", "warning")
            self._execute("powercfg -restoredefaultschemes")
            self.log("✅ Đã khôi phục!", "success")

    def _execute(self, command):
        """Execute command and log errors"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return True
        except subprocess.TimeoutExpired:
            self.log(f"⏱️ Timeout: {command[:50]}...", "warning")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)[:100]}", "error")
        return False
