import csv
from netmiko import ConnectHandler
from configparser import ConfigParser
import openpyxl

def read_config(filename):
    config = ConfigParser()
    config.read(filename)
    return config

def read_hosts(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        hosts = [row for row in reader]
    return hosts

def access_host_through_jump(jump_host, target_host, username, password):
    # Define parameters for jump host (Linux)
    jump_params = {
        'device_type': 'linux',  
        'host': jump_host['ip'],
        'username': username,
        'password': password,
    }

    # Define parameters for target host (Juniper)
    target_params = {
        'device_type': 'juniper_junos',  
        'host': target_host['ip'] if 'ip' in target_host else target_host['hostname'],
        'username': username,
        'password': password,
        'sock': (jump_host['ip'], 22),  
    }

    # Establish SSH connection to jump host
    with ConnectHandler(**jump_params) as jump_conn:
        # Establish SSH connection to target host via jump host
        with ConnectHandler(**target_params) as target_conn:
            # Run show configuration command
            output = target_conn.send_command("show configuration")
            return output

def main():
    config = read_config('config.ini')
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    hosts = read_hosts('hosts.csv')

    # Open or create Excel workbook
    workbook = openpyxl.load_workbook('results.xlsx')
    sheet = workbook.active

    # Iterate through hosts
    for host in hosts:
        try:
            # Access host through jump host and get configuration
            output = access_host_through_jump(
                {'ip': 'JUMP_HOST_IP'},  # Replace with jump host IP
                host,
                username,
                password
            )
            # Write output to Excel
            hostname = host.get('hostname', '')
            ip_address = host.get('ip', '')
            if not hostname:
                hostname = ip_address
            sheet.append([hostname, output])
            print(f"Successfully retrieved configuration from {hostname}")
        except Exception as e:
            print(f"Failed to retrieve configuration from {hostname}: {e}")

    # Save changes to Excel
    workbook.save('results.xlsx')

if __name__ == "__main__":
    main()
