import xml.etree.ElementTree as ET
from module.configManager import ConfigManager

def extract_plugins(xml_file):
    # 创建 ConfigParser 对象
    config = ConfigManager()

    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 遍历所有 plugin 标签
    for plugin in root.findall(".//plugin"):
        # 获取 filename 属性值作为键
        filename = plugin.get("filename")

        # 获取整个 plugin 标签及内容作为值
        plugin_content = ET.tostring(plugin, encoding="unicode")

        # 使用 set 方法添加或更新配置项
        config.set_value('pluginlist', filename, plugin_content)

    return True