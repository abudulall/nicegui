
import xml.etree.ElementTree as ET
from utils.tool_parserini2dict import parse_ini_file
from module.configManager import ConfigManager

tree = ET.ElementTree() 
config_manager = ConfigManager()

index = 0
kv = {}

plugin_index = 0
plugin_kv = {}

allow_add_plugin = {"world", "model", "link", "joint", "sensor"}

ini_plugin_dict = parse_ini_file(config_manager)

