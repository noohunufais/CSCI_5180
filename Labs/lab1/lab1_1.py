#!/usr/bin/env python3

import subprocess

oids ={ "Contact":"1.3.6.1.2.1.1.4.0",
 	"Name":"1.3.6.1.2.1.1.5.0",
 	"Location":"1.3.6.1.2.1.1.6.0",
 	"Number":"1.3.6.1.2.1.2.1.0",
	"Uptime":"1.3.6.1.2.1.1.3.0"
}

def ver1(oid):
    command = ["snmpwalk", "-v", "1", "-c", "public", "10.10.10.2", oid]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except:
        return "Error"

def ver2(oid):
    command = ["snmpwalk", "-v", "2c", "-c", "TSHOOT", "10.10.10.3", oid]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except:
        return "Error"

def ver3(oid):
    command = ["snmpwalk", "-v3", "-u", "MYUSER", "-l", "AuthPriv", "-a", "md5", "-A", "MYPASS123", "-x", "aes", "-X", "MYKEY123", "10.10.10.4", oid]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except:
        return "Error"


print("SNMPv1")

for key, value in oids.items():
    res = ver1(value)
    res = res.partition(":")
    print(f"{key} : {res[-1].strip()}")

print()

print("SNMPv2")

for key, value in oids.items():
    res = ver2(value)
    res = res.partition(":")
    print(f"{key} : {res[-1].strip()}")

print()

print("SNMPv3")

for key, value in oids.items():
    res = ver3(value)
    res = res.partition(":")
    print(f"{key} : {res[-1].strip()}")

