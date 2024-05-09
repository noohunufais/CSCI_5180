from datetime import datetime
from napalm import get_network_driver
from preliminaryChecks import preliminaryChecks
from threading import Thread

def getConfig(file):

    file_names = []
    def helper(router_ssh_info):
        driver = get_network_driver('ios')
        device = driver(hostname=router_ssh_info['ip'],username=router_ssh_info['username'],password=router_ssh_info['password'])
        device.open()
        output = device.get_config(retrieve='running',full=False)['running']
        hostname = device.get_facts()['hostname']
        current_utc_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        file_name = f"{hostname}_{current_utc_time}.txt"
        with open(file_name, "w") as file:
            file.write(output)
        file_names.append(file_name)

    ssh_info = preliminaryChecks(file)
    if not isinstance(ssh_info, dict):
        return ssh_info

    threads = []
    for router_ssh_info in ssh_info.values():
        thread = Thread(target=helper, args=(router_ssh_info,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    return file_names