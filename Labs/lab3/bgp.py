import json
import os
from prettytable import PrettyTable

def bgp_conf_info(file):

    with open(file,'r') as f:
        data = json.load(f)

    result = []

    for bgp_info in data['Routers'].values():
        bgp_commands = ["router bgp " + bgp_info['local_asn'], "neighbor " + bgp_info['neighbor_ip'] + " remote-as " + bgp_info['neighbor_remote_as']]
        network_commands = ["network " + network + " mask 255.255.255.255" for network in bgp_info['NetworkListToAdvertise']]
        bgp_commands.extend(network_commands)
        result.append(bgp_commands)

    return result

def bgp_neighbors_status(net_connect, router_name):
        output = net_connect.send_command("show ip bgp neighbors | include BGP")
        bgp_neighbor_ip = output.splitlines()[0].split()[3].strip(',')
        bgp_neighbor_as = output.splitlines()[0].split()[6].strip(',')
        bgp_neighbor_state = output.splitlines()[2].split()[3].strip(',')
        table = PrettyTable()
        table.field_names = ["BGP Neighbor IP", "BGP Neighbor AS", "BGP Neighbor State"]
        table.add_row([bgp_neighbor_ip, bgp_neighbor_as, bgp_neighbor_state])
        print(router_name)
        print(table)
        print()

def bgp_route_info(net_connect, router_name):
        table1 = PrettyTable()
        table1.field_names = ["Network","Next Hop"]
        output = net_connect.send_command("show ip bgp")
        for line in output.splitlines():
            if line.startswith("*>"):
                route_info = line[3:].split()
                network = route_info[0]
                next_hop =  route_info[1]
                table1.add_row([network, next_hop])
        print(router_name)
        print(table1)
        print()

def save_running_conf(net_connect, router_name):
    output = net_connect.send_command("show running-config")
    file_name = f"{router_name}_running_config.txt"
    with open(file_name, "w") as file:
        file.write(output)
    print(f"Saved running config of {router_name} to {file_name}")

def update_dict(net_connect, router_name, file):
    if router_name == "router_1":
        key = "R1"
    else:
        key = "R2"
    output = net_connect.send_command("show ip bgp neighbors | include BGP")
    bgp_neighbor_state = output.splitlines()[2].split()[3].strip(',')
    with open(file,'r') as f:
        data = json.load(f)
    data['Routers'][key]['neighbor_state'] = bgp_neighbor_state
    with open(file,'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully updated the bgp_conf file for {router_name}")
    