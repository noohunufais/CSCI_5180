from NMtcpdump import get_mac
from NMdhcp import conf_dhcpv4
from NMsnmp import snmp_get_interface_info, graph

# # Getting the mac addresses(add_2_3[0]) and IPv6 addresses(add_2_3[1]) of R2 and R3 from the pcap file.
# add_2_3 = get_mac("lab5.pcap","2001:4f10::cc69:72ff:fe36:f27e")  # VM IPv6 global

# ipv6_2_3 = add_2_3[1]
# mac_2_3 = add_2_3[0]

# # ping ipv6 2001:1234::C804:31FF:FECF:0
# dhcp_clients = conf_dhcpv4(ipv6_2_3, mac_2_3)
# print(dhcp_clients)

# community = "netman"
# targets = ['198.51.102.1', '198.51.101.2', '198.51.101.3', '198.51.100.4', '198.51.101.5']
# snmp_get_interface_info(community, targets)

# graph('1.3.6.1.4.1.9.9.109.1.1.1.1.6', 'netman', '198.51.102.1')



