from nicegui import ui
from module.ui import get_ui_container
from module.ui import add_attrib_lable_edit, add_text_lable_edit
from module.ui import save_tree
import xml.etree.ElementTree as ET
from module.global_variables import ini_plugin_dict
from module.global_variables import plugin_index, plugin_kv


tree_container, attrib_container, plugin_container, plugin_attrib_container = get_ui_container()

def on_plugin_tree_select(event):
    # pluginui界面
    global plugin_index
    global plugin_kv

    plugin_selected_path = event.value
    plugin_v_ele = plugin_kv[plugin_selected_path]

    plugin_attrib_container.clear()

    ele_attrib = plugin_v_ele.attrib
    # 添加attrib
    if len(ele_attrib):
        with plugin_attrib_container:
            ui.markdown('**属性**')
        for key, value in ele_attrib.items():
            add_attrib_lable_edit(plugin_attrib_container, plugin_v_ele, key, value)

    # 添加text
    if plugin_v_ele.text is not None and plugin_v_ele.text.strip() == '':
        pass
    else:
        with plugin_attrib_container:
            ui.markdown('**内容**')
        add_text_lable_edit(plugin_attrib_container, plugin_v_ele, plugin_v_ele.tag, plugin_v_ele.text)

def plugin_to_tree(plugin_element):
    plugin_tag = plugin_element.tag

    global plugin_index
    global plugin_kv
    plugin_tree_node = {'id': plugin_index}
    plugin_kv[plugin_index] = plugin_element
    plugin_index += 1

    plugin_tree_node['label'] = plugin_tag

    children = list(plugin_element)
    if children:
        plugin_tree_node['children'] = [plugin_to_tree(child) for child in children]
 
    return plugin_tree_node


class AgGridWrapper:
    def __init__(self, xml_ele):
        self.xml_ele = xml_ele
        self.init_data()
        # ui
        self.grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Id', 'field': 'id'},
                {'headerName': 'FileName', 'field': 'filename'},
            ],
            'rowData': self.row_data,
            'rowSelection': 'multiple',
        }).on('selectionChanged', self.view_modify_row)

        with ui.row():
            ui.button('Add', on_click=self.add_row)
            ui.button('Del', on_click=self.delete_selected_row)

    def init_data(self):
        self.row_data = []
        self.eles = []
        self.idx = 0
        children = list(self.xml_ele)
        if children:
            for child in children:
                if getattr(child, 'tag', '') == 'plugin':
                    self.row_data.append({'id': self.idx, 'filename': child.attrib['filename']})
                    self.eles.append(child)
                    self.idx += 1

    def update(self):
        self.init_data()
        self.grid.options['rowData'] = self.row_data
        self.grid.update()

    async def view_modify_row(self):
        plugin_container.clear()
        plugin_attrib_container.clear()
        row = await self.grid.get_selected_row()
        if row:
            clicked_ele = self.eles[row['id']]
            
        plugin_tree = plugin_to_tree(clicked_ele)
        with plugin_container: 
            ui.markdown('**插件属性树**')
            ui.tree([plugin_tree], on_select=on_plugin_tree_select)

    async def delete_selected_row(self):
        
        row = await self.grid.get_selected_row()
        if row:
            deleting_ele = self.eles[row['id']]
            deletename = deleting_ele.attrib['filename']

            self.xml_ele.remove(deleting_ele)
 
            save_tree(printcon=f'已删除{deletename}')

            plugin_container.clear()
            plugin_attrib_container.clear()
            self.update()
        else:
            ui.notify('没有选择行')

    def getListContexts(self):
        lc = []
        global ini_plugin_dict
        for key in ini_plugin_dict:
            lc.append(key)
        return lc
    
    def add_row(self):
        plugin_container.clear()
        plugin_attrib_container.clear()
        with plugin_container:
            continents = self.getListContexts()
            ui.select(options=continents, label='选择添加的插件', with_input=True, on_change=self.createplugin).classes('w-40')
            self.plugin_attrib = ui.column()
            with self.plugin_attrib:
                ui.button('Cancel', on_click=plugin_container.clear)
    
    def createplugin(self,e):
        # 创建一个 plugin 标签
        print(e.value)
        self.plugin_attrib.clear()
        plugin_attrib_container.clear()

        xml_string = ini_plugin_dict[e.value]
        parsed_element = ET.fromstring(xml_string)
        self.subroot = parsed_element
        # ui
        with self.plugin_attrib:
            ui.tree([plugin_to_tree(self.subroot)], on_select=on_plugin_tree_select)
            with ui.row():
                ui.button('Add', on_click=self.add_ok)
                ui.button('Cancel', on_click=self.add_cancel)
                
        
    def add_ok(self):
        self.xml_ele.append(self.subroot)
        add_plugin_name = self.subroot.attrib['filename']

        save_tree(printcon=f'已添加{add_plugin_name}')

        plugin_container.clear()
        plugin_attrib_container.clear()
        self.update()

    def add_cancel(self):
        plugin_container.clear()
        plugin_attrib_container.clear()

