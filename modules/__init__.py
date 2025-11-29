"""
Windows Optimizer Pro - Modular Architecture
Kiến trúc module hóa cho ứng dụng tối ưu Windows
"""

__version__ = "5.0.0"
__author__ = "Windows Optimizer Pro Team"

from .theme import ThemeManager
from .ui_components import ModernUI, ModernButton, Card, ScrollableFrame
from .base import BaseModule
from .system_module import SystemModule
from .optimization_module import OptimizationModule
from .software_module import SoftwareModule
from .network_module import NetworkModule
from .security_module import SecurityModule
from .files_module import FilesModule
from .resources_module import ResourcesModule

__all__ = [
    'ThemeManager',
    'ModernUI',
    'ModernButton',
    'Card',
    'ScrollableFrame',
    'BaseModule',
    'SystemModule',
    'OptimizationModule',
    'SoftwareModule',
    'NetworkModule',
    'SecurityModule',
    'FilesModule',
    'ResourcesModule'
]
