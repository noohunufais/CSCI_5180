from validateIP import check_ip
from connectivity import ping_check
from sshInfo import sshInfo
from netmiko import ConnectHandler
import bgp
from threading import Thread
from prettytable import PrettyTable

def dashboard():
    dashboard = "\nDashboard\n----------"
    print(dashboard)
    table = PrettyTable()
    functions_name = ["Configure BGP","Show BGP neighbors status","Show BGP route info","Save running-config","Update BGP conf dict"]
    numbers = [1, 2, 3, 4, 5]
    table.field_names = ["Function", "Number"]
    for func, num in zip(functions_name, numbers):
        table.add_row([func, num])
    table.align["Function"] = "l"
    table.align["Number"] = "r"
    print(table)
    func_number = int(input("\nEnter the function number: "))
    return func_number

def preliminaryChecks(file):

    ssh_info = sshInfo(file)
    if ssh_info == 0:
        print("SSH info file doesn't exist")
        return False
    
    ip_list = []
    for info in ssh_info.values():
        ip_list.append(info['ip'])

    flag = True
    for ip in ip_list:
        if not check_ip(ip):
            print(f'{ip} is not a valid IP address')
            flag = False
    if not flag:
        return False
    
    for ip in ip_list:
        if not ping_check(ip):
            print(f'{ip} is not pingable')
            flag = False
    if not flag:
        return False
    
    return ssh_info

def conf(router_name, ssh_info, bgp_conf_command,case_number):

    try:
        net_connect = ConnectHandler(**ssh_info)
        
        if case_number == 1:
            output = net_connect.send_config_set(bgp_conf_command)
            if '% ' in output:
                print(f"Wrong config command on {router_name}\nError:\n")
                print(output)
                print()
            else:
                print(f"Successfully configured {router_name}")
        elif case_number == 2:
            bgp.bgp_neighbors_status(net_connect, router_name)
        elif case_number == 3:
            bgp.bgp_route_info(net_connect, router_name)
        elif case_number == 4:
            bgp.save_running_conf(net_connect, router_name)
        elif case_number == 5:
            bgp.update_dict(net_connect, router_name, 'updated_dict.json')
        else:
            print("Enter a valid number!")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    func_number = dashboard()
    ssh_info = preliminaryChecks('sshInfo.json')
    if not ssh_info:
        return

    bgp_conf_commands = bgp.bgp_conf_info('bgp.conf')
    print()

    for i,j,k in zip(ssh_info.keys(),ssh_info.values(),bgp_conf_commands):
        thread = Thread(target=conf, args=(i,j,k,func_number,))
        thread.start()
        
if __name__ == "__main__":
    main()