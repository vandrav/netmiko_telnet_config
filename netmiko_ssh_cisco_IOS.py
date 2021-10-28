from netmiko import Netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import time


def write_to_file(input):
    with open("loguri.txt", "a") as textfile:
        textfile.write(str(input) + "\n")
    textfile.close()


user = input("Username: ")
password = getpass("Password: ")

with open('hosts.txt') as f:
    hosts = f.read().splitlines()

commands = '''
ip access-list standard allowed_vty
 remark --- Stablenet Agent 1
 permit host x.x.x.x
 remark --- Stablenet Agent 2
 permit host x.x.x.x
 remark --- FWI_NAT_mng_data_bi0514
 permit host x.x.x.x
 remark --- FWI_NAT_mng_data_cl0400
 permit host x.x.x.x
'''

cmds = commands.splitlines()

for HOST in hosts:

    cisco_device = {
        'host': HOST,
        'username': user,
        'password': password,
        'device_type': 'cisco_ios',
    }

    print("Connecting to host:", HOST)

    try:
        net_connect = Netmiko(**cisco_device)
        write_to_file(HOST)
    except NetMikoTimeoutException:
        print('Device not reachable')
        saveoutput = open("nefunctional.txt", "a")
        saveoutput.write(HOST)
        saveoutput.write("\t Unreachable")
        saveoutput.write("\n")
        continue
    except NetMikoAuthenticationException:
        print('Authentication Failure')
        saveoutput = open("nefunctional.txt", "a")
        saveoutput.write(HOST)
        saveoutput.write("\t Authentication Failure")
        saveoutput.write("\n")
        continue
    except SSHException:
        print('Make sure SSH is enabled')
        saveoutput = open("nefunctional.txt", "a")
        saveoutput.write(HOST)
        saveoutput.write("\t SSH is not enabled")
        saveoutput.write("\n")
        continue
    output = net_connect.send_command('term length 0')
    print(output)
    write_to_file(output)
    output = net_connect.send_config_set(cmds)
    print(output)
    write_to_file(output)
    output = net_connect.send_command('sh run | s allowed_vty')
    print(output)
    write_to_file(output)
    net_connect.disconnect()
