from nicegui import ui
from tkinter import filedialog
import subprocess
import sys
import os
from utils.tool_sdf2ini import extract_plugins
from module.configManager import ConfigManager
 


class MyMenu():
    def __init__(self):
        self.config_manager = ConfigManager()
        self.ini_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.ini_path = os.path.join(self.ini_dir, 'config.ini')

        ui.notify(f'配置文件路径为: {self.ini_path}')
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('选择输入sdf文件', on_click=self.selectInputFilePath)
                ui.menu_item('选择输出sdf文件', on_click=self.selectOutputFilePath)
                ui.separator()
                ui.menu_item('选择输入输出sdf文件', on_click=self.selectInputOutputFilePath, auto_close=False)
                ui.separator()
                ui.menu_item('从输入文件获取插件列表', on_click=self.GetPluginList)
                # ui.separator()
                # ui.menu_item('打开配置文件', on_click=self.OpenIniFile)
                ui.separator()
                ui.menu_item('显示输入输出文件路径', on_click=self.ShowInOutPath)
                ui.separator()
                ui.menu_item('Close', on_click=menu.close)
     
    def selectInputFilePath(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            ui.notify(f'取消设置')
            return
        ui.notify(f'设置输入sdf文件路径为: {file_path}')
        self.config_manager.set_value('Path', 'inputPath', file_path)


    def selectOutputFilePath(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            ui.notify(f'取消设置')
            return
        ui.notify(f'设置输出sdf文件路径为: {file_path}')
        self.config_manager.set_value('Path', 'outputPath', file_path)

    def selectInputOutputFilePath(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            ui.notify(f'取消设置')
            return
        ui.notify(f'设置输入输出sdf文件路径均为: {file_path}')
        self.config_manager.set_value('Path', 'inputPath', file_path)
        self.config_manager.set_value('Path', 'outputPath', file_path)


    def GetPluginList(self):
        inputPath = self.config_manager.get_value('Path', 'inputPath')
        if inputPath:
            if extract_plugins(inputPath):
                ui.notify(f'获取成功，刷新后使用')
            else:
                ui.notify(f'解析出错')
        else:
            ui.notify(f'找不到输入文件路径')

    def OpenIniFile(self):
        try:
            # 检查文件路径的有效性
            if not os.path.exists(self.ini_path):
                with open(self.ini_path, 'w') as f:
                    pass

            if not os.path.isfile(self.ini_path):
                raise ValueError(f"该路径不是一个文件: {self.ini_path}")

            # 检查文件权限
            if not os.access(self.ini_path, os.W_OK):
                raise PermissionError(f"对于文件没有写权限: {self.ini_path}")

            # 根据操作系统选择合适的方式打开文件
            if sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', self.ini_path])
            elif sys.platform.startswith('win'):
                os.startfile(self.ini_path)
            else:
                ui.notify(f'不支持的操作系统')
        except Exception as e:
            ui.notify(f'出错了')

    def ShowInOutPath(self):
        in_xml_file_path = self.config_manager.get_value('Path', 'inputPath')
        out_xml_file_path = self.config_manager.get_value('Path', 'outputPath')
        ui.notify(f'输入文件路径:{in_xml_file_path}')
        ui.notify(f'输出文件路径:{out_xml_file_path}')