import subprocess

command = ['sudo', 'nmap', '-sn', '172.20.74.0/24']

result = subprocess.run(command, capture_output=True, text=True, check=True)


with open('d.txt', 'a') as f:
        f.write(result.stdout)
        f.write('\n\n')