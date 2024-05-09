import yaml

def generate_yaml_files():

    tasks_main = [
        {
            "name": "Generate router configuration files",
            "template": {
                "src": "router.j2",
                "dest": "/etc/ansible/confs/{{ item.hostname }}.txt"
            },
            "with_items": "{{ routers }}"
        }
    ]


    site_yaml = [
        {
            "name": "Generate router configuration files",
            "hosts": "localhost",
            "roles": ["router"]
        }
    ]

    routers_info = [
        {
            "hostname": "R1",
            "fa0/0": {"ip": "198.51.100.1", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "fa1/0": {"ip": "198.51.101.1", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "fa1/1": {"ip": "198.51.102.1", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "loopback1": {"ip": "10.0.0.1", "subnet_mask": "255.255.255.255", "wildcard": "0.0.0.0"},
            "ospf_process_id": 1,
            "ospf_area": 0
        },
        {
            "hostname": "R2",
            "fa0/0": {"ip": "198.51.100.2", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "fa1/0": {"ip": "198.51.101.2", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "loopback1": {"ip": "20.0.0.1", "subnet_mask": "255.255.255.255", "wildcard": "0.0.0.0"},
            "ospf_process_id": 1,
            "ospf_area": 0       
        },
        {
            "hostname": "R3",
            "fa0/0": {"ip": "198.51.100.3", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.255"},
            "fa1/0": {"ip": "198.51.102.3", "subnet_mask": "255.255.255.0", "wildcard": "0.0.0.0"},
            "loopback1": {"ip": "30.0.0.1", "subnet_mask": "255.255.255.255", "wildcard": "0.0.0.255"},
            "ospf_process_id": 1,
            "ospf_area": 0
        }
    ]


    with open("roles/router/tasks/main.yaml", "w") as file:
        yaml.dump(tasks_main, file, sort_keys=False)

    with open("router_config.yaml", "w") as file:
        yaml.dump(site_yaml, file, sort_keys=False)

    with open("roles/router/vars/main.yaml", "w") as file:
        yaml.dump({"routers": routers_info}, file, sort_keys=False)
    

def main():
    generate_yaml_files()

if __name__ == "__main__":
    main()
