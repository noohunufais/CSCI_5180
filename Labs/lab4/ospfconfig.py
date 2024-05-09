from napalm import get_network_driver

def ospfConfig(ospf_config):

    driver = get_network_driver('ios')
    device = driver(hostname=ospf_config['ip'],username=ospf_config['username'],password=ospf_config['password'])
    device.open()
    interface = device.get_interfaces_ip()
    ip_list = []
    for interface in interface.values():
        for ipv4 in interface.values():
            for ip in ipv4.keys():
                ip_list.append(ip)

    print(ip_list)


    command = 'router ospf ' + ospf_config['ospf_process_id'] + '\n'

    network = ['network '+ ospf_config['loopback_ip'] + ' 0.0.0.0 area ' + ospf_config['ospf_area_id'] ]

    network = '\n'.join(network)

    command = command + network
    print(command)

    device.load_merge_candidate(config=command) 
    print(device.compare_config()) 
    device.commit_config()
    device.close()