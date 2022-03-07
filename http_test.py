import psutil
import traceback

def get_local_ip():
    '''获取当前使用的IP'''
    try:
        interface_data = psutil.net_if_stats()
        interface_address_information = psutil.net_if_addrs()
        # print(interface_address_information)
        key_list = list(interface_data.keys())
        for key in key_list:
            if '以太网' in key or 'WLAN' in key:
                if interface_data[key].isup == True:
                    addr_info_list = interface_address_information[key]
                    for addr_info in addr_info_list:
                        if addr_info.family == 2:
                            return addr_info.address
        return None
    except Exception as e:
        print(traceback.print_exc())
if __name__ == '__main__':
    ip = get_local_ip()
    print(ip)