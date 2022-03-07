import re
from shuncom_module.shuncom_fun import *

def shuncom_device_list(agreement):
    """
    返回网关的ip、Mac、ip和Mac列表
    return app_get_ip_list,app_get_mac_list,app_get_device_list,app_get_gwver_list
    """
    udp_recv_dict = {}
    try:
        # gw_ip = get_net_card()[0]
        # mac_ip_255 = str(re.findall(r'(?<!\d)\d{1,3}\.\d{1,3}\.\d{1,3}(?=\.\d)', gw_ip)[0]) + '.255'
        ip_port = ('192.168.8.211', 8887)  # 网关的网段端口
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.settimeout(10)  # 获取套接字默认超时时间10秒
        udp_client.bind(('', 9999))  # 电脑ip和端口
        send_data = agreement
        udp_client.sendto(send_data, ip_port)  # 发送数据

        try:
            while True:
                device_list, addr = udp_client.recvfrom(8888)
                device_list = aes_decrypt(device_list)
                device_list['addr'] = addr
                print('device_list %s, addr %s' % (device_list, addr))
        except Exception as e:
            udp_client.close()
            print(udp_recv_dict)
    except Exception as Error:
        print(traceback.print_exc())

if __name__ == "__main__":
    t = time.time()

    send_data1 = '''{
	"timestamp": 1601196762389,
	"messageId": "20997980",
	"passwd" : "shuncom_Administrator_login",
	"module":"sysinfo",
	"properties": ["macaddr", "HW_model", "version", "proto"],
	"topic": "/+/+/properties_read",
	"type": "sub"
}'''
    send_data2 = '''{
	"timestamp": 1601196762389,
	"messageId": "20997980",
	"passwd" : "shuncom_Administrator_login",
	"module":"bdinfo",
	"properties":["MODULE"],
	"topic": "/+/+/properties_read",
	"type": "sub"
}'''
    send_data3 = '''{
	"timestamp": 1601196762389,
	"messageId": "20997980",
	"passwd" : "shuncom_Administrator_login",
	"deviceId": "2c6a6f00adb5",
	"function":"network_read",
	"properties": ["ip", "http_port", "netmask"],
	"topic": "/+/+/function_invoke",
	"type": "sub"
}'''
    send_data4 = '''{
	"timestamp": 1601196762389,
	"messageId": "20997980",
	"deviceId": "2c6a6f00adb5",
	"passwd": "shuncom_Administrator_login",
	"function":"cloud_config_read",
	"properties": ["sziot", "sztt_cloud", "mqtt_server"],
	"topic": "/+/+/function_invoke",
	"type": "sub"
}'''
    reboot_order = '''{
      "timestamp": 1601196762389,
      "messageId": "20997980",
      "deviceId": "2c6a6f00adb5",
      "function":"reboot",
      "passwd":"shuncom_Administrator_login",
      "topic": "/+/+/function_invoke",
      "type": "sub"
    }'''
    send_data = aes_encrypt(send_data4)
    print(send_data)
    shuncom_device_list(send_data)


