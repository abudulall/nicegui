// libtest_plugin.c
#include <stdio.h>
#include <stdlib.h>

char* get_plugin_config() {
    const char* template = 
        "<plugin filename=\"PluginImuBroadcastDriveGZ\" name=\"Drive::ImuBroadcastDriveUnit\">\n"
        "  <ServerIp>%s</ServerIp>\n"
        "  <ServerPort>%s</ServerPort>\n"
        "  <topic>%s</topic>\n"
        "</plugin>\n";

    const char* server_ip = "127.0.0.1";
    const char* server_port = "8886";
    const char* topic = "imu";

    size_t length = snprintf(NULL, 0, template, server_ip, server_port, topic) + 1;

    char* xml_string = (char*)malloc(length);

    snprintf(xml_string, length, template, server_ip, server_port, topic);

    return xml_string;
}
