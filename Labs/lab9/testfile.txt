from netmiko import ConnectHandler
import unittest

def test_one():
    r3_mgmt_ip = ''
    username = ''
    password = ''

    with open('info.csv','r') as file:
        data = file.readlines()

        for line in data:
            if 'Router3' in line:
                r3_mgmt_ip = line.split(',')[1]
                username = line.split(',')[2]
                password = line.split(',')[3]

    device = {
            'device_type': 'cisco_ios',
            'host': r3_mgmt_ip,
            'username': username,
            'password': password, 
        }

    net_connect = ConnectHandler(**device)

    output = net_connect.send_command('show ip interface loopback 99 | inc Internet address is')

    r3_lb_ip = output.split()[-1]

    return r3_lb_ip

def test_two():
    r1_mgmt_ip = ''
    username = ''
    password = ''

    with open('info.csv','r') as file:
        data = file.readlines()

        for line in data:
            if 'R1' in line:
                r1_mgmt_ip = line.split(',')[1]
                username = line.split(',')[2]
                password = line.split(',')[3]

    device = {
            'device_type': 'cisco_ios',
            'host': r1_mgmt_ip,
            'username': username,
            'password': password, 
        }

    net_connect = ConnectHandler(**device)

    output = net_connect.send_command('show ip ospf database | inc Area')

    areas = [int(area[-2]) for area in output.split('\n')]
    
    return sum(areas)

def test_three():
    r2_mgmt_ip = ''
    username = ''
    password = ''
    r2_lb_ip = ''
    r5_lb_ip = ''

    with open('info.csv','r') as file:
        data = file.readlines()

        for line in data:
            if 'Router2' in line:
                r2_mgmt_ip = line.split(',')[1]
                username = line.split(',')[2]
                password = line.split(',')[3]
                r2_lb_ip = line.split(',')[6]
            if 'Router5' in line:
                r5_lb_ip = line.split(',')[6]

    device = {
            'device_type': 'cisco_ios',
            'host': r2_mgmt_ip,
            'username': username,
            'password': password, 
        }

    net_connect = ConnectHandler(**device)

    output = net_connect.send_command(f'ping {r5_lb_ip} source {r2_lb_ip}')

    success_rate = int(output.split("percent")[0].split()[-1])

    return success_rate

class TestMathFunctions(unittest.TestCase):
    def test_check_r3_loopback(self):
        r3_lb_ip = test_one()
        self.assertEqual(r3_lb_ip,"10.1.3.1/24")

    def test_r1_has_single_area(self):
        sum_of_areas = test_two()
        self.assertEqual(sum_of_areas, 0)

    def test_ping_r2_to_r5(self):
        success_rate = test_three()
        self.assertGreater(success_rate, 0)


if __name__ == '__main__':
    unittest.main()