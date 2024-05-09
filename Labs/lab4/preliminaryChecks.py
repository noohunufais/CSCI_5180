from sshInfo import sshInfo
from validateIP import check_ip
from connectivity import ping_check


def preliminaryChecks(file):

    ssh_info = sshInfo(file)
    if ssh_info == 0:
        return f"SSH info file doesn't exist"
    
    ip_list = []
    for info in ssh_info.values():
        ip_list.append(info['ip'])

    wrong_ip_list = []

    flag = True
    for ip in ip_list:
        if not check_ip(ip):
            wrong_ip_list.append(ip)
            flag = False
    if not flag:
        return f'List of invalid IP addresses: {wrong_ip_list}'
    
    for ip in ip_list:
        if not ping_check(ip):
            wrong_ip_list.append(ip)
            flag = False
    if not flag:
        return f'List of non-pingable IP addresses: {wrong_ip_list}'
    
    return ssh_info