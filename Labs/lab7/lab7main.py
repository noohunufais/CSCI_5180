import subprocess
import os
from netmiko import ConnectHandler
from threading import Thread
from loguru import logger
import re

def ping_check(host):
    try:
        subprocess.run(["ping", "-c", "1", host], stdout=subprocess.DEVNULL, timeout=1)
        return True
    except Exception as e:
        return False
    

def set_and_get_config(net_connect,host_name,ip):

    file_location = f'/etc/ansible/confs/{host_name}.txt'
    
    if not os.path.exists(file_location):
        logger.error(f'There is no configuration file for {host_name}')
        return

    with open(file_location,'r') as file:
        configurations = file.readlines()

    commands = [ command.strip() for command in configurations if command.strip() != '' ]

    net_connect.send_config_set(commands)
    logger.success(f'Successfully configured {host_name}')


    ip_interface_brief = net_connect.send_command("show ip interface brief")
    print(f'\nInterface details for {host_name}\n')
    print(ip_interface_brief)

    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    ip_addresses = re.findall(pattern, ip_interface_brief)

    print()
    for ip in ip_addresses:
        if ping_check(ip):
            logger.success(f'{ip} is pingable')
        else:
            logger.warning(f'{ip} is not pingable')

def main():
    
    hosts = {   
                'R1':'198.51.100.1', 
                'R2':'198.51.100.2',
                'R3':'198.51.100.3'
    }

    device = {
        'device_type': 'cisco_ios',
        'username': 'nufais',
        'password': 'netman', 
    }

    threads = []

    for host_name, ip in hosts.items():
        device['host'] = ip

        if not ping_check(ip):
            logger.error(f'{host_name} is not reachable')
            continue     

        net_connect = ConnectHandler(**device)
        print("\n-----------------------------------------------------------------------\n")
        logger.info(f"Connected to {host_name}")


        thread = Thread(target=set_and_get_config, args=(net_connect,host_name,ip,))
        threads.append(thread)
        thread.start()
    
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
