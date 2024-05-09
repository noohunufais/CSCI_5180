from ncclient import manager
from ncclient.operations import TimeoutExpiredError
import csv
from threading import Thread
from netmiko import ConnectHandler
import ipaddress
from prettytable import PrettyTable

def wildcard_to_subnet_mask(wildcard_mask):

    octects = wildcard_mask.split('.')
    first = 255 - int(octects[0])
    second = 255 - int(octects[1])
    third = 255 - int(octects[2])
    fourth = 255 - int(octects[3])

    return str(first) + '.' + str(second) + '.' + str(third) + '.' + str(fourth)

def set_config(m, mgmt_ip, hostname, loopback_name, loopback_ip, loopback_subnet,area, network_to_advertise, wildcard):

    lb_ip_address = loopback_ip.split('/')[0]

    configs = f'''
        <config>
            <cli-config-data>
                <cmd>hostname {hostname}</cmd>
                <cmd>interface {loopback_name}</cmd>
                <cmd>ip address {lb_ip_address} {loopback_subnet}</cmd>
                <cmd>router ospf 1</cmd>
                <cmd>network {mgmt_ip} 0.0.0.0 area 0</cmd>
                <cmd>network {network_to_advertise} {wildcard} area {area}</cmd>
            </cli-config-data>
        </config>
    '''

    try:
        m.edit_config(target='running', config=configs, default_operation=None, test_option=None, error_option=None)

    except TimeoutExpiredError:
        print(f"Successfully configured on {hostname}")

def get_config(router_ip, table):
    device = {
        'device_type': 'cisco_ios',
        'host': router_ip,
        'username': 'lab',
        'password': 'lab123', 
    }

    net_connect = ConnectHandler(**device)

    hostname = net_connect.send_command("show running-config | inc hostname")
    hostname = hostname.split()[1]

    loopback_99_ip = net_connect.send_command("show ip interface loopback 99 | inc Internet")
    loopback_99_ip = loopback_99_ip.split()[3]

    advertised_networks = net_connect.send_command("show ip protocols | sec Routing for Networks:")
    advertised_networks = advertised_networks.splitlines()[1:]

    advertised_networks_list = []

    for advertised_network in advertised_networks:
    
        network = advertised_network.split()[0]
        wildcard_mask = advertised_network.split()[1]
        area = advertised_network.split()[3]

        subnet_mask = wildcard_to_subnet_mask(wildcard_mask)

        advertised_network_cidr = str(ipaddress.IPv4Network(network + '/' + subnet_mask, strict=False))

        advertised_networks_list.append(advertised_network_cidr)


    table.add_row([hostname,loopback_99_ip, area, advertised_networks_list])

def netconf_config(config,table):
    ip = config[1]
    username = config[2]
    password = config[3]
    m =  manager.connect(
        host=ip,
        username= username,
        password=password,
        port=22,  
        hostkey_verify=False, 
        look_for_keys =False,
        allow_agent = False,
        timeout=8
    )

    set_config(m,ip,config[4],config[5],config[6],config[7],config[8],config[9],config[10])

    get_config(config[1],table)

def main():
    configs = []
    with open("info.csv", 'r') as file:
        data = csv.reader(file)
        next(data)
        for row in data:
            configs.append(row)

    table = PrettyTable()
    table.field_names = ['Hostname','Loopback 99 IP','OSPF area','OSPF Network to advertise']

    threads = []
    for config in configs:
        thread = Thread(target=netconf_config, args=(config,table,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(table)

if __name__ =="__main__":
    main()