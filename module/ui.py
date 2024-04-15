from nicegui import ui
from module.global_variables import tree, config_manager
from module.menu import MyMenu

def save_tree(isprint=True, printcon=''):
    # 持久化 配置文件
    config_manager.save_config()

    # 持久化 xml文件
    in_xml_file_path = config_manager.get_value('Path', 'inputPath')
    xml_file_path = config_manager.get_value('Path', 'outputPath')
    if in_xml_file_path and xml_file_path:
        tree.write(xml_file_path)
        if printcon:
            ui.notify(printcon)
        elif isprint:
            ui.notify(f'保存sdf文件到:{xml_file_path}')
    else :
        if isprint:
            ui.notify(f'找不到输入或输出文件路径')


def add_attrib_lable_edit(container, ele, key, v):
    with container:
        ui.input(key, value=v, on_change=lambda e: ele.set(key, e.value)) \
            .props('input-style="color: blue" input-class="font-mono"')

def add_text_lable_edit(container, ele, key, v):
    def cb(e):
        ele.text = e.value

    with container:
        ui.input(key, value=v, on_change=cb) \
            .props('input-style="color: blue" input-class="font-mono"')


# ui_builder.py
# 单例模式
class UIManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._build_ui()
        return cls._instance

    def _build_ui(self):
        with ui.row().classes('w-full items-center'):
            ui.space()
            self.freshbtn = ui.button(text='刷新')
            self.savebtn = ui.button(icon='save')
            MyMenu()
        with ui.row().classes('w-full'):
            self.tree_container = ui.column()
            ui.space()
            with ui.column():
                self.attrib_container = ui.scroll_area().classes('w-96 h-96')  
                self.plugin_container = ui.scroll_area().classes('w-96 h-96') 
                self.plugin_attrib_container = ui.scroll_area().classes('w-96 h-96') 

ui_manager = UIManager()

# 获取ui管理器实例
def get_ui_manager():
    return ui_manager


# 获取ui常用容器
def get_ui_container():
    return ui_manager.tree_container, ui_manager.attrib_container, ui_manager.plugin_container, ui_manager.plugin_attrib_container