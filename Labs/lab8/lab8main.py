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

def cidr_to_ip_subnet_wildcard(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    
    network_address = str(network.network_address)
    subnet_mask = str(network.netmask)
    wild_card = str(network.hostmask)
    
    return network_address, subnet_mask, wild_card

def set_config(m, hostname, loopback_ip, area, network_to_advertise):

    lb_network_address, lb_subnet_mask, lb_wild_card = cidr_to_ip_subnet_wildcard(loopback_ip)
    ospf_network_address, ospf_subnet_mask, ospf_wild_card = cidr_to_ip_subnet_wildcard(network_to_advertise)

    lb_ip_address = loopback_ip.split('/')[0]

    configs = f'''
        <config>
            <cli-config-data>
                <cmd>hostname {hostname}</cmd>
                <cmd>interface loopback 99</cmd>
                <cmd>ip address {lb_ip_address} {lb_subnet_mask}</cmd>
                <cmd>router ospf 1</cmd>
                <cmd>network {ospf_network_address} {ospf_wild_card} area {area}</cmd>
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
    ip = config[2]
    m =  manager.connect(
        host=ip,
        username='lab',
        password='lab123',
        port=22,  
        hostkey_verify=False, 
        look_for_keys =False,
        allow_agent = False,
        timeout=8
    )

    set_config(m,config[1],config[3],config[4],config[5])

    get_config(config[2],table)

def main():
    configs = []
    with open("lab9-obj2-conf.csv", 'r') as file:
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
