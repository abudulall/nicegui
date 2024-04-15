import xml.dom.minidom
import re
import xml.etree.ElementTree as ET

def format_xml(input_file, output_file):
    # 解析 XML 文件
    tree = ET.parse(input_file)

    # 获取 ElementTree 的根元素
    root = tree.getroot()

    # 使用 minidom 格式化 XML，去掉额外的空白行
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = re.sub(r'\n\s*\n', '\n', xml_string)
    # 写入格式化后的 XML 到文件
    with open(output_file, 'w') as file:
        file.write(xml_string)

# # 示例用法
# input_xml_file = 'modified_xml_file.xml'  # 替换为你的 XML 文件路径
# output_xml_file = 'output.xml'  # 替换为输出 XML 文件路径
# format_xml(input_xml_file, output_xml_file)

