import configparser
import os
import sys

class ConfigManager:
    _instance = None

    def __new__(cls, config_file='config.ini'):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config_file = config_file
            cls._instance._config = configparser.ConfigParser()
            # 禁用键名大小写转换
            cls._instance._config.optionxform = lambda option: option

            # 检查配置文件是否存在，如果不存在则创建并写入示例配置
            if not cls._instance._config.read(cls._instance._config_file):
                cur_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
                outputpath = os.path.join(cur_dir, 'output.sdf')
                cls._instance._config['Path'] = {'outputPath': outputpath}
                if not cls._instance._config.has_section('pluginlist'):  # 这里调用 has_section 方法
                    cls._instance._config.add_section('pluginlist')
                with open(cls._instance._config_file, 'w') as configfile:
                    cls._instance._config.write(configfile)
 
        return cls._instance

    def get_value(self, section, key):
        """
            获取指定 section 和 key 的值
        """
        if self._config.has_section(section) and self._config.has_option(section, key):
            return self._config.get(section, key)
        else:
            return None

    def set_value(self, section, key, value):
        """
            设置指定 section 和 key 的值
        """
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, value)
        self.save_config()

    def save_config(self):
        # 保存配置文件
        with open(self._config_file, 'w') as configfile:
            self._config.write(configfile)