from module.global_variables import ini_plugin_dict, index, kv, plugin_index, plugin_kv
from module.global_variables import allow_add_plugin, tree, config_manager
from module.agGridWrapper import AgGridWrapper
from nicegui import ui
from utils.tool_parserini2dict import parse_ini_file

from module.ui import get_ui_container, save_tree
from module.ui import add_attrib_lable_edit, add_text_lable_edit
tree_container, attrib_container, plugin_container, plugin_attrib_container = get_ui_container()


def flesh_tree():
    # 读取配置文件，配置plugin列表
    global ini_plugin_dict, config_manager
    ini_plugin_dict.clear()
    ini_plugin_dict.update(parse_ini_file(config_manager))
    
    # 读取输入 xml文件
    xml_file_path = config_manager.get_value('Path', 'inputPath')
    if xml_file_path:
        tree.parse(xml_file_path, None)
        root_element1 = tree.getroot()
        nicegui_tree1 = xml_to_tree(root_element1)

        # 容器清空
        tree_container.clear()
        attrib_container.clear()
        plugin_container.clear()
        plugin_attrib_container.clear()

        with tree_container:
            ui.tree([nicegui_tree1], on_select=on_tree_select)
    else:
        ui.notify('设置输入sdf文件来展示xml树')


def on_tree_select(event):
    selected_path = event.value
    if selected_path is None:
        return
    
    save_tree(isprint=False)

    # 清除pluginui界面
    global plugin_index
    global plugin_kv
    plugin_index = 0
    plugin_kv = {}

    xml_ele = kv[selected_path]

    attrib_container.clear()
    plugin_container.clear()
    plugin_attrib_container.clear()

    ele_attrib = xml_ele.attrib
    # 添加attrib
    if len(ele_attrib):
        with attrib_container:
            ui.markdown('**属性**')
        for key, value in ele_attrib.items():
            add_attrib_lable_edit(attrib_container, xml_ele, key, value)

    # 添加text
    if xml_ele.text is not None and xml_ele.text.strip() == '':
        print("该标签没有文本内容")
    else:
        with attrib_container:
            ui.markdown('**内容**')
        add_text_lable_edit(attrib_container, xml_ele, xml_ele.tag, xml_ele.text)

    if xml_ele.tag in allow_add_plugin:
        with attrib_container:
            ui.markdown('**插件**')
            AgGridWrapper(xml_ele)

def xml_to_tree(xml_element):
    ele_tag = xml_element.tag
    if(ele_tag == 'link' or ele_tag == 'joint'):
        ele_attrib = xml_element.attrib
        ele_tag += '__'
        ele_tag += ele_attrib['name']

    global index
    global kv
    tree_node = {'id': index}
    kv[index] = xml_element
    index += 1

    tree_node['label'] = ele_tag

    children = list(xml_element)
    if children:
        tree_node['children'] = [xml_to_tree(child) for child in children if getattr(child, 'tag', '') != 'plugin']

    return tree_node
