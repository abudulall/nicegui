from nicegui import ui, native
from module.ui import get_ui_container, get_ui_manager, save_tree
from module.global_variables import tree, config_manager
from module.showtree import flesh_tree, xml_to_tree, on_tree_select

if __name__ == '__main__':
    # ui
    tree_container, attrib_container, plugin_container, plugin_attrib_container = get_ui_container()
    ui_manager = get_ui_manager()
    ui_manager.freshbtn.on('click', flesh_tree)
    ui_manager.savebtn.on('click', save_tree)

    # 读取 XML 文件
    xml_file_path = config_manager.get_value('Path', 'inputPath')
    if xml_file_path:
        tree.parse(xml_file_path, None)
        root_element = tree.getroot()
        # 转换为 nicegui 树形结构
        nicegui_tree = xml_to_tree(root_element)
        with tree_container:
            ui.tree([nicegui_tree], on_select=on_tree_select)
    else:
        ui.notify('设置输入sdf文件来展示xml树')


    ui.run(reload=False, port=native.find_open_port())