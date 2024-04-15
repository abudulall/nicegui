
def parse_ini_file(config_manager):
    # 创建字典来存储结果
    result_dict = {}

    # 遍历 ConfigParser 对象中的节和键值对
    for filename, value in config_manager._config.items('pluginlist'):
        # 将 filename 和 value 存储在结果字典中
        result_dict[filename] = value

    return result_dict
