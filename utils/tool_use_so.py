# -*- coding: utf-8 -*-
import os
from ctypes import *
# 定义键值对结构体
print(1)
# 加载动态链接库
so = cdll.LoadLibrary(os.getcwd() + "/libPluginDiffDriveIGN.so")
print(2)
# 设置返回类型为 POINTER(KeyValuePair) 表示返回的是结构体数组
so.get_plugin_config.restype = c_char_p

# 调用函数
result = so.get_plugin_config().decode()

# 打印结果
print(result)
# from cffi import FFI
# import os

# ffi = FFI()

# # 加载动态链接库
# so = ffi.dlopen(os.getcwd() + "/libPluginDiffDriveIGN.so")

# # 定义键值对结构体
# ffi.cdef("""
#     char* get_plugin_config();
# """)

# # 调用函数
# result = ffi.string(so.get_plugin_config()).decode()

# # 打印结果
# print(result)