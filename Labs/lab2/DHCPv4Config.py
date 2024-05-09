from netmiko import ConnectHandler
from threading import Thread
from loguru import logger

cisco_ios= {
    'device_type':'cisco_ios', 
    'username':'nufais', 
    'password':'netman'
}

def conf(ip):
    logger.info("start")

    net_connect = ConnectHandler(**cisco_ios,ip = ip)
    commands = ["interface FastEthernet 0/1", "ip address dhcp", "no shutdown"]
    output = net_connect.send_config_set(commands)
    print(output)
    
    logger.info("end")

def main():
    ip_list = [ '10.10.10.2', '10.10.10.3', '10.10.10.4' ]

    for ip in ip_list:
        thread = Thread(target=conf, args=(ip,))
        thread.start()

if __name__ == "__main__":
    main()