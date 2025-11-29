"""
Security Module - FULL FEATURES
Module bảo mật hệ thống với UAC, Defender, Firewall chi tiết
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class SecurityModule(BaseModule):
    """Module bảo mật - Full Features"""

    def get_module_info(self):
        return {
            'icon': '🔐',
            'name': 'Bảo mật',
            'description': 'Cài đặt bảo mật và UAC control',
            'category': 'security'
        }

    def create_ui(self):
        """Tạo UI - Security Settings"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🔐 Bảo mật hệ thống",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # UAC Card
        uac_card = Card(content.scrollable_frame, title="🛡️ User Account Control (UAC)")
        uac_card.pack(fill='x', pady=(0, 16))

        # UAC info
        tk.Label(
            uac_card.content_frame,
            text="Mức độ bảo mật UAC:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(anchor='w', pady=(8, 4))

        # UAC buttons
        uac_btns = tk.Frame(uac_card.content_frame, bg=self.colors['bg_card'])
        uac_btns.pack(fill='x', pady=8)

        ModernButton(
            uac_btns, "Cao nhất",
            command=lambda: self.set_uac_level(4),
            icon="🔴", style='danger', width=100, height=32
        ).pack(side='left', padx=4)

        ModernButton(
            uac_btns, "Cao",
            command=lambda: self.set_uac_level(3),
            icon="🟠", style='warning', width=100, height=32
        ).pack(side='left', padx=4)

        ModernButton(
            uac_btns, "Trung bình",
            command=lambda: self.set_uac_level(2),
            icon="🟡", style='secondary', width=110, height=32
        ).pack(side='left', padx=4)

        ModernButton(
            uac_btns, "Tắt (Nguy hiểm!)",
            command=lambda: self.set_uac_level(0),
            icon="⚠️", style='danger', width=150, height=32
        ).pack(side='left', padx=4)

        tk.Label(
            uac_card.content_frame,
            text="⚠️ Thay đổi UAC yêu cầu khởi động lại máy",
            bg=self.colors['bg_card'],
            fg=self.colors['warning'],
            font=ModernUI.FONTS['small']
        ).pack(anchor='w', pady=4)

        # Windows Defender Card
        defender_card = Card(content.scrollable_frame, title="🛡️ Windows Defender")
        defender_card.pack(fill='x', pady=(0, 16))

        # Real-time Protection
        defender_row1 = tk.Frame(defender_card.content_frame, bg=self.colors['bg_card'])
        defender_row1.pack(fill='x', pady=8)

        ModernButton(
            defender_row1, "Bật Real-time Protection",
            command=lambda: self.toggle_defender_realtime(True),
            icon="✅", style='success', width=200, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            defender_row1, "Tắt Real-time Protection",
            command=lambda: self.toggle_defender_realtime(False),
            icon="⚠️", style='danger', width=200, height=36
        ).pack(side='left', padx=4)

        # Cloud Protection
        defender_row2 = tk.Frame(defender_card.content_frame, bg=self.colors['bg_card'])
        defender_row2.pack(fill='x', pady=8)

        ModernButton(
            defender_row2, "Bật Cloud Protection",
            command=lambda: self.toggle_defender_cloud(True),
            icon="☁️", style='info', width=180, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            defender_row2, "Tắt Cloud Protection",
            command=lambda: self.toggle_defender_cloud(False),
            icon="⚠️", style='warning', width=180, height=36
        ).pack(side='left', padx=4)

        # Sample Submission
        defender_row3 = tk.Frame(defender_card.content_frame, bg=self.colors['bg_card'])
        defender_row3.pack(fill='x', pady=8)

        ModernButton(
            defender_row3, "Bật Sample Submission",
            command=lambda: self.toggle_defender_sample(True),
            icon="📤", style='primary', width=190, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            defender_row3, "Tắt Sample Submission",
            command=lambda: self.toggle_defender_sample(False),
            icon="⚠️", style='warning', width=190, height=36
        ).pack(side='left', padx=4)

        # Open Windows Security
        defender_row4 = tk.Frame(defender_card.content_frame, bg=self.colors['bg_card'])
        defender_row4.pack(fill='x', pady=8)

        ModernButton(
            defender_row4, "Mở Windows Security",
            command=self.open_windows_security,
            icon="🛡️", style='info', width=180, height=36
        ).pack(side='left', padx=4)

        tk.Label(
            defender_card.content_frame,
            text="⚠️ Tắt Windows Defender có thể làm hệ thống dễ bị tấn công!",
            bg=self.colors['bg_card'],
            fg=self.colors['danger'],
            font=ModernUI.FONTS['body_bold']
        ).pack(anchor='w', pady=4)

        # BitLocker Card
        bitlocker_card = Card(content.scrollable_frame, title="🔒 BitLocker Encryption")
        bitlocker_card.pack(fill='x', pady=(0, 16))

        bitlocker_btns = tk.Frame(bitlocker_card.content_frame, bg=self.colors['bg_card'])
        bitlocker_btns.pack(fill='x', pady=8)

        ModernButton(
            bitlocker_btns, "Tắt BitLocker tất cả ổ đĩa",
            command=self.disable_bitlocker_all,
            icon="🔓", style='danger', width=200, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            bitlocker_btns, "Kiểm tra trạng thái BitLocker",
            command=self.check_bitlocker_status,
            icon="🔍", style='info', width=220, height=36
        ).pack(side='left', padx=4)

        tk.Label(
            bitlocker_card.content_frame,
            text="⚠️ Tắt BitLocker sẽ giải mã dữ liệu - có thể mất nhiều thời gian!",
            bg=self.colors['bg_card'],
            fg=self.colors['warning'],
            font=ModernUI.FONTS['small']
        ).pack(anchor='w', pady=4)

        # Windows Firewall Card
        firewall_card = Card(content.scrollable_frame, title="🔥 Windows Firewall")
        firewall_card.pack(fill='x', pady=(0, 16))

        firewall_btns = tk.Frame(firewall_card.content_frame, bg=self.colors['bg_card'])
        firewall_btns.pack(fill='x', pady=8)

        ModernButton(
            firewall_btns, "Bật Firewall",
            command=lambda: self.toggle_firewall(True),
            icon="✅", style='success', width=130, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            firewall_btns, "Tắt Firewall",
            command=lambda: self.toggle_firewall(False),
            icon="⚠️", style='danger', width=130, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            firewall_btns, "Mở Firewall Settings",
            command=self.open_firewall_settings,
            icon="⚙️", style='info', width=180, height=36
        ).pack(side='left', padx=4)

        # SmartScreen Card
        smartscreen_card = Card(content.scrollable_frame, title="🔍 SmartScreen Filter")
        smartscreen_card.pack(fill='x', pady=(0, 16))

        smartscreen_btns = tk.Frame(smartscreen_card.content_frame, bg=self.colors['bg_card'])
        smartscreen_btns.pack(fill='x', pady=8)

        ModernButton(
            smartscreen_btns, "Bật SmartScreen",
            command=lambda: self.toggle_smartscreen(True),
            icon="✅", style='success', width=150, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            smartscreen_btns, "Tắt SmartScreen",
            command=lambda: self.toggle_smartscreen(False),
            icon="⚠️", style='warning', width=150, height=36
        ).pack(side='left', padx=4)

        tk.Label(
            smartscreen_card.content_frame,
            text="SmartScreen bảo vệ khỏi phishing và malware khi tải file",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['small']
        ).pack(anchor='w', pady=4)

        # Windows Update Card
        update_card = Card(content.scrollable_frame, title="🔄 Windows Update")
        update_card.pack(fill='x', pady=(0, 16))

        update_btns = tk.Frame(update_card.content_frame, bg=self.colors['bg_card'])
        update_btns.pack(fill='x', pady=8)

        ModernButton(
            update_btns, "Bật Auto Update",
            command=lambda: self.toggle_windows_update(True),
            icon="✅", style='success', width=140, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            update_btns, "Tắt Auto Update",
            command=lambda: self.toggle_windows_update(False),
            icon="⚠️", style='warning', width=150, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            update_btns, "Kiểm tra Update",
            command=self.check_windows_update,
            icon="🔍", style='info', width=140, height=36
        ).pack(side='left', padx=4)

        # Console
        self.create_console(main)
        self.log("Module Bảo mật đã sẵn sàng", "success")

        return main

    def set_uac_level(self, level):
        """Set UAC level (0=Off, 2=Medium, 3=High, 4=Highest)"""
        level_names = {0: 'Tắt', 2: 'Trung bình', 3: 'Cao', 4: 'Cao nhất'}
        level_name = level_names.get(level, 'Không xác định')

        if level == 0:
            if not self.confirm("⚠️ CẢNH BÁO BẢO MẬT",
                              "Tắt UAC làm giảm bảo mật nghiêm trọng!\n"
                              "Malware có thể chạy với quyền admin mà không cảnh báo.\n\n"
                              "Bạn có chắc muốn tiếp tục?"):
                return

        self.log(f"🛡️ Đang đặt UAC level: {level_name}...", "info")

        def set_level():
            try:
                # ConsentPromptBehaviorAdmin values:
                # 0 = No prompt (UAC disabled)
                # 2 = Prompt on secure desktop (Highest)
                # 5 = Prompt for consent for non-Windows binaries (High)

                if level == 0:
                    consent_value = 0
                    prompt_value = 0
                elif level == 2:
                    consent_value = 5
                    prompt_value = 1
                elif level == 3:
                    consent_value = 5
                    prompt_value = 1
                elif level == 4:
                    consent_value = 2
                    prompt_value = 1
                else:
                    consent_value = 5
                    prompt_value = 1

                # Set registry values
                subprocess.run(
                    f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d {consent_value} /f',
                    shell=True, timeout=10
                )
                subprocess.run(
                    f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v PromptOnSecureDesktop /t REG_DWORD /d {prompt_value} /f',
                    shell=True, timeout=10
                )

                self.log(f"✅ Đã đặt UAC level: {level_name}", "success")
                self.log("⚠️ Cần khởi động lại máy để áp dụng!", "warning")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=set_level, daemon=True).start()

    def toggle_defender_realtime(self, enable):
        """Toggle Windows Defender Real-time Protection - CHUYÊN SÂU"""
        action = "Bật" if enable else "Tắt"

        if not enable:
            if not self.confirm("⚠️ CẢNH BÁO BẢO MẬT",
                              "Tắt Real-time Protection làm hệ thống dễ bị tấn công!\n\n"
                              "Bạn có chắc muốn tiếp tục?"):
                return

        self.log(f"🛡️ Đang {action} Defender một cách chuyên sâu...", "info")

        def toggle():
            try:
                if not enable:
                    # TẮT HOÀN TOÀN DEFENDER - Chuyên sâu

                    # 1. Tắt tất cả tính năng qua PowerShell
                    commands = [
                        'Set-MpPreference -DisableRealtimeMonitoring $true',
                        'Set-MpPreference -DisableBehaviorMonitoring $true',
                        'Set-MpPreference -DisableBlockAtFirstSeen $true',
                        'Set-MpPreference -DisableIOAVProtection $true',
                        'Set-MpPreference -DisablePrivacyMode $true',
                        'Set-MpPreference -DisableScriptScanning $true',
                        'Set-MpPreference -SubmitSamplesConsent 2',
                        'Set-MpPreference -MAPSReporting 0',
                        'Set-MpPreference -HighThreatDefaultAction 6 -Force',
                        'Set-MpPreference -ModerateThreatDefaultAction 6',
                        'Set-MpPreference -LowThreatDefaultAction 6',
                        'Set-MpPreference -SevereThreatDefaultAction 6',
                    ]

                    for cmd in commands:
                        try:
                            subprocess.run(f'powershell -Command "{cmd}"', shell=True, timeout=15, capture_output=True)
                        except:
                            pass

                    self.log("  • Đã tắt tất cả tính năng Defender qua PowerShell", "info")

                    # 2. Tắt qua Registry - Disable Antivirus
                    reg_commands = [
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiVirus /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableIOAVProtection /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableScanOnRealtimeEnable /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Reporting" /v DisableEnhancedNotifications /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\SpyNet" /v DisableBlockAtFirstSeen /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\SpyNet" /v SpynetReporting /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\SpyNet" /v SubmitSamplesConsent /t REG_DWORD /d 2 /f',
                    ]

                    for cmd in reg_commands:
                        try:
                            subprocess.run(cmd, shell=True, timeout=10, capture_output=True)
                        except:
                            pass

                    self.log("  • Đã tắt Defender qua Registry", "info")

                    # 3. Tắt các Services liên quan
                    services = [
                        'WinDefend',  # Windows Defender Service
                        'WdNisSvc',   # Windows Defender Network Inspection
                        'WdNisDrv',   # Windows Defender Network Inspection Driver
                        'WdFilter',   # Windows Defender Mini-Filter Driver
                        'Sense',      # Windows Defender Advanced Threat Protection
                    ]

                    for service in services:
                        try:
                            subprocess.run(f'sc stop {service}', shell=True, timeout=10, capture_output=True)
                            subprocess.run(f'sc config {service} start= disabled', shell=True, timeout=10, capture_output=True)
                        except:
                            pass

                    self.log("  • Đã tắt các Services Defender", "info")

                    # 4. Tắt Defender qua Task Scheduler
                    try:
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Disable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Disable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Disable', shell=True, timeout=10, capture_output=True)
                        self.log("  • Đã tắt các Task Scheduler của Defender", "info")
                    except:
                        pass

                    self.log("✅ Đã TẮT HOÀN TOÀN Windows Defender!", "success")
                    self.log("⚠️ Khởi động lại máy để áp dụng đầy đủ!", "warning")

                else:
                    # BẬT LẠI DEFENDER

                    # 1. Bật lại qua PowerShell
                    commands = [
                        'Set-MpPreference -DisableRealtimeMonitoring $false',
                        'Set-MpPreference -DisableBehaviorMonitoring $false',
                        'Set-MpPreference -DisableBlockAtFirstSeen $false',
                        'Set-MpPreference -DisableIOAVProtection $false',
                        'Set-MpPreference -DisablePrivacyMode $false',
                        'Set-MpPreference -DisableScriptScanning $false',
                        'Set-MpPreference -SubmitSamplesConsent 1',
                        'Set-MpPreference -MAPSReporting 2',
                    ]

                    for cmd in commands:
                        try:
                            subprocess.run(f'powershell -Command "{cmd}"', shell=True, timeout=15, capture_output=True)
                        except:
                            pass

                    # 2. Xóa Registry keys
                    subprocess.run(r'reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /f', shell=True, timeout=10, capture_output=True)

                    # 3. Bật lại Services
                    services = ['WinDefend', 'WdNisSvc', 'Sense']
                    for service in services:
                        try:
                            subprocess.run(f'sc config {service} start= auto', shell=True, timeout=10, capture_output=True)
                            subprocess.run(f'sc start {service}', shell=True, timeout=10, capture_output=True)
                        except:
                            pass

                    # 4. Bật lại Tasks
                    try:
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Enable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Enable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Enable', shell=True, timeout=10, capture_output=True)
                        subprocess.run(r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Enable', shell=True, timeout=10, capture_output=True)
                    except:
                        pass

                    self.log("✅ Đã BẬT LẠI Windows Defender!", "success")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def toggle_defender_cloud(self, enable):
        """Toggle Windows Defender Cloud Protection"""
        action = "Bật" if enable else "Tắt"
        self.log(f"☁️ Đang {action} Defender Cloud Protection...", "info")

        def toggle():
            try:
                subprocess.run(
                    f'powershell -Command "Set-MpPreference -MAPSReporting {2 if enable else 0}"',
                    shell=True, timeout=30
                )
                self.log(f"✅ Đã {action} Defender Cloud Protection!", "success")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def toggle_defender_sample(self, enable):
        """Toggle Windows Defender Sample Submission"""
        action = "Bật" if enable else "Tắt"
        self.log(f"📤 Đang {action} Defender Sample Submission...", "info")

        def toggle():
            try:
                subprocess.run(
                    f'powershell -Command "Set-MpPreference -SubmitSamplesConsent {1 if enable else 2}"',
                    shell=True, timeout=30
                )
                self.log(f"✅ Đã {action} Defender Sample Submission!", "success")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def open_windows_security(self):
        """Open Windows Security"""
        self.log("🛡️ Đang mở Windows Security...", "info")
        try:
            subprocess.Popen('start windowsdefender:', shell=True)
            self.log("✅ Đã mở Windows Security!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def toggle_firewall(self, enable):
        """Toggle Windows Firewall - CHUYÊN SÂU"""
        action = "Bật" if enable else "Tắt"

        if not enable:
            if not self.confirm("⚠️ CẢNH BÁO BẢO MẬT",
                              "Tắt Firewall làm hệ thống dễ bị tấn công từ mạng!\n\n"
                              "Bạn có chắc muốn tiếp tục?"):
                return

        self.log(f"🔥 Đang {action} Windows Firewall chuyên sâu...", "info")

        def toggle():
            try:
                if not enable:
                    # TẮT HOÀN TOÀN FIREWALL - Chuyên sâu

                    # 1. Tắt tất cả profiles (Domain, Private, Public)
                    profiles = ['domainprofile', 'privateprofile', 'publicprofile', 'allprofiles']
                    for profile in profiles:
                        try:
                            subprocess.run(
                                f'netsh advfirewall set {profile} state off',
                                shell=True, timeout=10, capture_output=True
                            )
                            subprocess.run(
                                f'netsh advfirewall set {profile} firewallpolicy allowinbound,allowoutbound',
                                shell=True, timeout=10, capture_output=True
                            )
                        except:
                            pass

                    self.log("  • Đã tắt tất cả Firewall profiles", "info")

                    # 2. Tắt Windows Firewall service
                    try:
                        subprocess.run('net stop mpssvc', shell=True, timeout=10, capture_output=True)
                        subprocess.run('sc config mpssvc start= disabled', shell=True, timeout=10, capture_output=True)
                        self.log("  • Đã tắt dịch vụ Windows Firewall", "info")
                    except:
                        pass

                    # 3. Tắt qua Registry
                    reg_commands = [
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile" /v EnableFirewall /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile" /v EnableFirewall /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile" /v EnableFirewall /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile" /v DoNotAllowExceptions /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile" /v DoNotAllowExceptions /t REG_DWORD /d 0 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile" /v DoNotAllowExceptions /t REG_DWORD /d 0 /f',
                    ]

                    for cmd in reg_commands:
                        try:
                            subprocess.run(cmd, shell=True, timeout=10, capture_output=True)
                        except:
                            pass

                    self.log("  • Đã tắt Firewall qua Registry", "info")

                    # 4. Xóa tất cả Firewall rules (tùy chọn - cẩn thận!)
                    try:
                        subprocess.run('netsh advfirewall firewall delete rule name=all', shell=True, timeout=30, capture_output=True)
                        self.log("  • Đã xóa tất cả Firewall rules", "info")
                    except:
                        pass

                    self.log("✅ Đã TẮT HOÀN TOÀN Windows Firewall!", "success")

                else:
                    # BẬT LẠI FIREWALL

                    # 1. Bật lại service
                    try:
                        subprocess.run('sc config mpssvc start= auto', shell=True, timeout=10, capture_output=True)
                        subprocess.run('net start mpssvc', shell=True, timeout=10, capture_output=True)
                        self.log("  • Đã bật dịch vụ Windows Firewall", "info")
                    except:
                        pass

                    # 2. Bật tất cả profiles
                    profiles = ['domainprofile', 'privateprofile', 'publicprofile', 'allprofiles']
                    for profile in profiles:
                        try:
                            subprocess.run(
                                f'netsh advfirewall set {profile} state on',
                                shell=True, timeout=10, capture_output=True
                            )
                            subprocess.run(
                                f'netsh advfirewall set {profile} firewallpolicy blockinbound,allowoutbound',
                                shell=True, timeout=10, capture_output=True
                            )
                        except:
                            pass

                    self.log("  • Đã bật tất cả Firewall profiles", "info")

                    # 3. Khôi phục Registry
                    reg_commands = [
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile" /v EnableFirewall /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile" /v EnableFirewall /t REG_DWORD /d 1 /f',
                        r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile" /v EnableFirewall /t REG_DWORD /d 1 /f',
                    ]

                    for cmd in reg_commands:
                        try:
                            subprocess.run(cmd, shell=True, timeout=10, capture_output=True)
                        except:
                            pass

                    self.log("  • Đã bật Firewall qua Registry", "info")

                    # 4. Reset về cài đặt mặc định
                    try:
                        subprocess.run('netsh advfirewall reset', shell=True, timeout=30, capture_output=True)
                        self.log("  • Đã reset Firewall về mặc định", "info")
                    except:
                        pass

                    self.log("✅ Đã BẬT LẠI Windows Firewall!", "success")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def open_firewall_settings(self):
        """Open Windows Firewall Settings"""
        self.log("⚙️ Đang mở Firewall Settings...", "info")
        try:
            subprocess.Popen('firewall.cpl', shell=True)
            self.log("✅ Đã mở Firewall Settings!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def toggle_smartscreen(self, enable):
        """Toggle SmartScreen Filter"""
        action = "Bật" if enable else "Tắt"
        self.log(f"🔍 Đang {action} SmartScreen...", "info")

        def toggle():
            try:
                value = "Warn" if enable else "Off"
                # For Edge/Chrome
                subprocess.run(
                    f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v SmartScreenEnabled /t REG_SZ /d {value} /f',
                    shell=True, timeout=10
                )
                # For Apps
                subprocess.run(
                    f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppHost" /v EnableWebContentEvaluation /t REG_DWORD /d {1 if enable else 0} /f',
                    shell=True, timeout=10
                )
                self.log(f"✅ Đã {action} SmartScreen!", "success")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def toggle_windows_update(self, enable):
        """Toggle Windows Auto Update"""
        action = "Bật" if enable else "Tắt"
        self.log(f"🔄 Đang {action} Windows Auto Update...", "info")

        def toggle():
            try:
                if enable:
                    # Enable update service
                    subprocess.run('sc config wuauserv start= auto', shell=True, timeout=10)
                    subprocess.run('net start wuauserv', shell=True, timeout=10)
                else:
                    # Disable update service
                    subprocess.run('net stop wuauserv', shell=True, timeout=10)
                    subprocess.run('sc config wuauserv start= disabled', shell=True, timeout=10)

                self.log(f"✅ Đã {action} Windows Auto Update!", "success")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=toggle, daemon=True).start()

    def check_windows_update(self):
        """Open Windows Update"""
        self.log("🔍 Đang mở Windows Update...", "info")
        try:
            subprocess.Popen('start ms-settings:windowsupdate', shell=True)
            self.log("✅ Đã mở Windows Update!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def disable_bitlocker_all(self):
        """Tắt BitLocker trên tất cả ổ đĩa - CHUYÊN SÂU"""
        if not self.confirm("⚠️ CẢNH BÁO BẢO MẬT",
                          "Tắt BitLocker sẽ GIẢI MÃ tất cả dữ liệu!\n"
                          "Quá trình này có thể mất vài giờ tùy dung lượng.\n\n"
                          "Bạn có chắc muốn tiếp tục?"):
            return

        self.log("🔒 Đang tắt BitLocker trên tất cả ổ đĩa...", "info")

        def disable():
            try:
                # 1. Lấy danh sách tất cả ổ đĩa có BitLocker
                result = subprocess.run(
                    'manage-bde -status',
                    shell=True, capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    output = result.stdout
                    # Parse để tìm các ổ đĩa
                    import re
                    drives = re.findall(r'([C-Z]:)', output)

                    if drives:
                        self.log(f"  • Tìm thấy {len(drives)} ổ đĩa: {', '.join(set(drives))}", "info")

                        # 2. Tắt BitLocker trên từng ổ
                        for drive in set(drives):
                            try:
                                self.log(f"  • Đang tắt BitLocker trên {drive}...", "info")
                                subprocess.run(
                                    f'manage-bde -off {drive}',
                                    shell=True, timeout=60, capture_output=True
                                )
                                self.log(f"  ✓ Đã bắt đầu giải mã {drive}", "success")
                            except Exception as e:
                                self.log(f"  ✗ Lỗi khi tắt {drive}: {str(e)}", "warning")

                        # 3. Tắt dịch vụ BitLocker
                        try:
                            subprocess.run('sc stop BDESVC', shell=True, timeout=10, capture_output=True)
                            subprocess.run('sc config BDESVC start= disabled', shell=True, timeout=10, capture_output=True)
                            self.log("  • Đã tắt dịch vụ BitLocker", "info")
                        except:
                            pass

                        # 4. Tắt qua Registry
                        reg_commands = [
                            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\BitLocker" /v PreventDeviceEncryption /t REG_DWORD /d 1 /f',
                            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\FVE" /v EnableBDEWithNoTPM /t REG_DWORD /d 0 /f',
                            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\FVE" /v UseAdvancedStartup /t REG_DWORD /d 0 /f',
                        ]

                        for cmd in reg_commands:
                            try:
                                subprocess.run(cmd, shell=True, timeout=10, capture_output=True)
                            except:
                                pass

                        self.log("✅ Đã bắt đầu tắt BitLocker trên tất cả ổ đĩa!", "success")
                        self.log("⚠️ Quá trình giải mã đang chạy ngầm, có thể mất vài giờ!", "warning")
                        self.log("💡 Dùng 'manage-bde -status' để kiểm tra tiến độ", "info")
                    else:
                        self.log("ℹ️ Không tìm thấy ổ đĩa nào có BitLocker bật", "info")
                else:
                    self.log("❌ Không thể kiểm tra trạng thái BitLocker", "error")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=disable, daemon=True).start()

    def check_bitlocker_status(self):
        """Kiểm tra trạng thái BitLocker"""
        self.log("🔍 Đang kiểm tra trạng thái BitLocker...", "info")

        def check():
            try:
                result = subprocess.run(
                    'manage-bde -status',
                    shell=True, capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    output = result.stdout

                    # Parse output
                    import re
                    drives = re.findall(r'([C-Z]:)', output)

                    if drives:
                        self.log(f"📊 Tìm thấy {len(set(drives))} ổ đĩa:", "info")

                        # Hiển thị trạng thái chi tiết
                        for line in output.split('\n'):
                            if ':' in line and any(keyword in line for keyword in ['Protection', 'Encryption', 'Conversion', 'Size']):
                                self.log(f"  {line.strip()}", "info")
                    else:
                        self.log("ℹ️ Không có ổ đĩa nào được BitLocker quản lý", "info")
                else:
                    self.log("❌ Không thể kiểm tra trạng thái", "error")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=check, daemon=True).start()
