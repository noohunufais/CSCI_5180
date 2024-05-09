from netmiko import ConnectHandler
from NMtcpdump import get_mac

def convert_mac_to_client_id(mac_2_3):
    client_id_list = []
    for mac in mac_2_3:
        client_id = mac.split('.')
        client_id = '01' + client_id[0][:2] + '.' + client_id[0][2:] + client_id[1][:2] + '.' + client_id[1][2:] + client_id[2][:2] + '.' + client_id[2][2:]
        client_id_list.append(client_id)
    return client_id_list

def conf_dhcpv4(ipv6_2_3, mac_2_3):
    client_id_list = convert_mac_to_client_id(mac_2_3)
    device = {
        'device_type': 'cisco_ios',
        'host': '198.51.100.4',    # R4's IP address
        'username': 'nufais',
        'password': 'netman', 
    }

    net_connect = ConnectHandler(**device)

    command = 'show ipv6 neighbors fastEthernet 0/0'

    output = net_connect.send_command(command)

    output_lines = output.strip().split('\n')[1:]

    ipv6_5 = ''
    for line in output_lines:
        line = line.split()[0].lower()
        if line not in ipv6_2_3 and line.startswith('2001'):
            ipv6_5 = line

    net_connect.disconnect()
    
    device['host'] = ipv6_5

    net_connect = ConnectHandler(**device)

    # commands = ['interface FastEthernet 0/0', 'ip address 198.51.101.5 255.255.255.0']
    # output = net_connect.send_config_set(commands)
    # print(output)
    
    # commands = ['ip dhcp pool R2', 'host 198.51.101.2 255.255.255.0', f'client-identifier {client_id_list[0]}']
    # output = net_connect.send_config_set(commands)
    # print(output)

    # commands = ['ip dhcp pool R3', 'host 198.51.101.3 255.255.255.0', f'client-identifier {client_id_list[1]}']
    # output = net_connect.send_config_set(commands)
    # print(output)

    # commands = ['ip dhcp pool MYPOOL', 'network 198.51.101.0 255.255.255.0']
    # output = net_connect.send_config_set(commands)
    # print(output)
        
    output = net_connect.send_command('show ip dhcp binding')
    return output
