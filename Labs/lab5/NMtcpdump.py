from scapy.all import rdpcap
import ipaddress

def extract_ipv6(file, pc_ipv6):

    packets = rdpcap(file)
    ipv6_list = []
    
    for packet in packets:
        if 'IPv6' in packet and packet['IPv6'].dst == pc_ipv6 and packet['IPv6'].src not in ipv6_list:
            ipv6_list.append(packet['IPv6'].src)

    return ipv6_list

def extract_mac(ipv6_list):
    mac_list = []
    for ipv6 in ipv6_list:
        ipv6 = format(ipaddress.IPv6Address(ipv6), '_X').split('_')

        first = list(bin(int(ipv6[-4], 16)))[2:]

        if first[6] == '0':
            first[6] = '1'
        else:
            first[6] = '0'

        first = str(hex(int(''.join(first), 2)))[2:]
    
        mac = first + "." + ipv6[-3][:-2] + ipv6[-2][2:] + "." +  ipv6[-1]
        mac_list.append(mac.lower())
    
    return mac_list

def get_mac(file, pc_ipv6):
    ipv6_list = extract_ipv6(file, pc_ipv6)
    mac_list =  extract_mac(ipv6_list)
    return [mac_list, ipv6_list]

