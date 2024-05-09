from pysnmp.hlapi import *
from threading import Thread
from json import dump
import matplotlib.pyplot as plt
from netmiko import ConnectHandler
from time import sleep

routers_info = {}

def snmp_walk(oid, community, target):
    for (error_indication,
         error_status,
         error_index,
         var_binds) in nextCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((target, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity(oid)),
                               lexicographicMode=False):
        if error_indication:
            print(f"SNMP error: {error_indication}")
            break
        elif error_status:
            print(f"SNMP error: {error_status}")
            break
        else:
            for var_bind in var_binds:
                yield var_bind
        
def get_interface_info(community, target):

    device_info = {}

    device_name = ''
    for var_bind in snmp_walk('1.3.6.1.2.1.1.5', community, target):  # Device name
        device_name = str(var_bind[1]).split('.')[0]
        routers_info[device_name] = { 'addresses':{}, 'status':{}}

    for var_bind in snmp_walk('1.3.6.1.2.1.4.20.1.2', community, target): # Active interface index number and its IP address
        index_number = str(var_bind[1])
        ip = '.'.join(str(var_bind[0]).split('.')[-4:])
        device_info[index_number] = [ip]

    for var_bind in snmp_walk('1.3.6.1.2.1.31.1.1.1.1', community, target): # Interface name
        index = str(var_bind[0])[-1]
        interface_name = str(var_bind[1])
        if index in device_info:
            device_info[index].append(interface_name) 

    for var_bind in snmp_walk('1.3.6.1.2.1.4.20.1.3', community, target): # IP address and its subnet mask
        ip = '.'.join(str(var_bind[0]).split('.')[-4:])
        subnet_mask = '.'.join(str(var_bind).split('=')[1].strip().split(".")[-4:])
        for key, value in device_info.items():
            if ip in value[0]:
                device_info[key].append(subnet_mask)

    for var_bind in snmp_walk('1.3.6.1.2.1.2.2.1.8', community, target): # Interface status
        index = str(var_bind[0])[-1]
        if index in device_info:
            if str(var_bind[1]) == '1':
                device_info[index].append('Up') 
            else:
                device_info[index].append('Down') 

    for value in device_info.values():
        routers_info[device_name]['addresses'][value[1]] = { 'v4':{value[0]:value[2]}, 'v6':{} }
        routers_info[device_name]['status'][value[1]] = value[3]

    device = {
            'device_type': 'cisco_ios',
            'username': 'nufais',
            'password': 'netman', 
        }
    device['host'] = target

    net_connect = ConnectHandler(**device)

    command = 'show ipv6 interface fastEthernet 0/0 | sec Global'

    output = net_connect.send_command(command)

    if output:

        output = output.split('\n')[1].strip().split()

        routers_info[device_name]['addresses']['Fa0/0']['v6'] = {output[0].strip(','):output[3]}
        # print(output[0].strip(','))
        # print(output[3])

    command = 'show ipv6 interface fastEthernet 1/0 | sec Global'

    output = net_connect.send_command(command)

    if output:

        output = output.split('\n')[1].strip().split()
        routers_info[device_name]['addresses']['Fa1/0']['v6'] = {output[0].strip(','):output[3]}
        # print(output[0].strip(','))
        # print(output[3])

    net_connect.disconnect()


def snmp_get_interface_info(community, targets):


    threads = []
    for target in targets:

        thread = Thread(target=get_interface_info, args=(community, target,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with open('router_info.txt', 'w') as file:
        dump(routers_info, file, indent=4)         

def graph(oid, community, target):

    x = [x for x in range(0,120,5)]

    y = []
    
    for _ in range(24):
        for var_bind in snmp_walk(oid, community, target):
            print(int(var_bind[1]))
            y.append(int(var_bind[1]))

        sleep(5)
    
    print(y)

    plt.plot(x,y)
    plt.xlabel('Time(Sec)')
    plt.ylabel('CPU utilization(%)')
    plt.title('CPU utilization of R1')
    plt.show()




    


