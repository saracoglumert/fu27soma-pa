#!/usr/bin/python3
import subprocess
import urllib.request
import yaml
import pathlib
import os
import inspect
import shutil
import fileinput
import datetime
import time
import urllib
import sys

with open('config.yaml', 'r') as file:
    CONF_YAML = yaml.safe_load(file)

CONF_DEBUG = CONF_YAML['manage']['debug']
CONF_ROOT_PATH = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
CONF_TEMP_PATH = CONF_ROOT_PATH + "/" + CONF_YAML['manage']['path_temp']
CONF_RES_PATH = CONF_ROOT_PATH + "/" + CONF_YAML['manage']['path_resources']

class Tools:
    @staticmethod
    def ReplaceInplace(file,old,new):
        with fileinput.FileInput(file, inplace=True) as file:
            for line in file:
                print(line.replace(old, new), end='')

    @staticmethod
    def Call(command):
        if CONF_DEBUG:
            subprocess.call(command,shell=True)
        else:
            subprocess.call(command,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    @staticmethod
    def Template():
        if not os.path.exists(CONF_YAML['host']['container_template_path']):
            print('[all] \t\t Downloading container template...')
            urllib.request.urlretrieve(CONF_YAML['host']['container_template_url'],CONF_YAML['host']['container_template_path'])

    @staticmethod
    def Ping(host):
        result = subprocess.run('ping -c 1 {}'.format(host), capture_output=True, shell=True).stdout.decode()
        if "Unreachable" in result:
            return False
        else:
            return True

    @staticmethod
    def Help():
        print("./manage config \t Run configuration helper.")
        print("./manage build \t\t Build containers.")
        print("./manage update \t Update files.")
        print("./manage start \t\t Start services.")
        print("./manage stop \t\t Stop services.")
        print("./manage restart \t Restart services.")
        print("./manage reboot \t Reboot containers.")
        print("./manage help \t\t Shows this help page.")

    @staticmethod
    def Config():
        print("[network] \t\t Checking network...")
        gateway = subprocess.run('/sbin/ip route | awk \'/default/ { print $3 }\'', capture_output=True, shell=True).stdout.decode().replace('\n','')
        base = '.'.join(gateway.split('.')[:-1]) + "."
        ips = []
        results = []
        for i in range(0,256,50):
            ip_server = base+str(i)
            ip_node1 = base+str(i+1)
            ip_node2 = base+str(i+2)
            ips.append((ip_server,ip_node1,ip_node2))
        for element in ips:
            temp = 0
            for element2 in element:
                if not Tools.Ping(element2):
                    temp = temp + 1
            if temp == 3:
                results.append(element)
        print("\nGateway   : {}\n".format(gateway))
        print("Options are : \n")
        for result in results:
            print("Server - ID : {} / IP : {}".format(result[0].split(".")[-1],result[0]))
            print("Node 1 - ID : {} / IP : {}".format(result[1].split(".")[-1],result[1]))
            print("Node 2 - ID : {} / IP : {}".format(result[2].split(".")[-1],result[2]))
            print("-"*os.get_terminal_size()[0])

    @staticmethod
    def SetSSH():
        Tools.Call("ssh-keygen -R {}".format(CONF_YAML['server']['network_ip']))
        Tools.Call("ssh-keygen -R {}".format(CONF_YAML['node1']['network_ip']))
        Tools.Call("ssh-keygen -R {}".format(CONF_YAML['node2']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_hosts'],CONF_YAML['server']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_hosts'],CONF_YAML['node1']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_hosts'],CONF_YAML['node2']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_keys'],CONF_YAML['server']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_keys'],CONF_YAML['node1']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh_keys'],CONF_YAML['node2']['network_ip']))

class Containers:
    @staticmethod
    def Create():
        # Check for template
        Tools.Template()
        
        # Create containers
        print('[server] \t Creating container...')
        # Container - server
        Tools.Call('pct create {} {} --hostname "{}" --nameserver "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,ip={},gw={},hwaddr={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
            CONF_YAML['server']['id'],
            CONF_YAML['host']['container_template_path'],
            CONF_YAML['server']['network_hostname'],
            CONF_YAML['host']['network_dns'],
            CONF_YAML['host']['container_memory'],
            CONF_YAML['server']['network_ip']+"/"+str(CONF_YAML['host']['network_cidr']),
            CONF_YAML['host']['network_gateway'],
            CONF_YAML['server']['network_mac'],
            CONF_YAML['host']['container_disk'],
            CONF_YAML['host']['container_pass'],
            CONF_YAML['host']['ssh_keys']))
        print('[node1] \t Creating container...')
        # Container - node1
        Tools.Call('pct create {} {} --hostname "{}" --nameserver "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,ip={},gw={},hwaddr={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
            CONF_YAML['node1']['id'],
            CONF_YAML['host']['container_template_path'],
            CONF_YAML['node1']['network_hostname'],
            CONF_YAML['host']['network_dns'],
            CONF_YAML['host']['container_memory'],
            CONF_YAML['node1']['network_ip']+"/"+str(CONF_YAML['host']['network_cidr']),
            CONF_YAML['host']['network_gateway'],
            CONF_YAML['node1']['network_mac'],
            CONF_YAML['host']['container_disk'],
            CONF_YAML['host']['container_pass'],
            CONF_YAML['host']['ssh_keys']))
        print('[node2] \t Creating container...')
        # Container - node2
        Tools.Call('pct create {} {} --hostname "{}" --nameserver "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,ip={},gw={},hwaddr={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
            CONF_YAML['node2']['id'],
            CONF_YAML['host']['container_template_path'],
            CONF_YAML['node2']['network_hostname'],
            CONF_YAML['host']['network_dns'],
            CONF_YAML['host']['container_memory'],
            CONF_YAML['node2']['network_ip']+"/"+str(CONF_YAML['host']['network_cidr']),
            CONF_YAML['host']['network_gateway'],
            CONF_YAML['node2']['network_mac'],
            CONF_YAML['host']['container_disk'],
            CONF_YAML['host']['container_pass'],
            CONF_YAML['host']['ssh_keys']))

    @staticmethod
    def Start():
        print('[all] \t\t Starting containers...')
        Tools.Call('pct start {}'.format(CONF_YAML['server']['id']))
        Tools.Call('pct start {}'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct start {}'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Reboot():
        print('[all] \t\t Rebooting containers...')
        Tools.Call('pct reboot {}'.format(CONF_YAML['server']['id']))
        Tools.Call('pct reboot {}'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct reboot {}'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Stop():
        print('[all] \t\t Stopping containers...')
        Tools.Call('pct stop {}'.format(CONF_YAML['server']['id']))
        Tools.Call('pct stop {}'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct stop {}'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Destroy():
        Containers.Stop()
        print('[all] \t\t Destroying containers...')
        Tools.Call('pct destroy {}'.format(CONF_YAML['server']['id']))
        Tools.Call('pct destroy {}'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct destroy {}'.format(CONF_YAML['node2']['id']))    

    @staticmethod
    def Build():    
        print('[server] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/scripts/build.sh'.format(CONF_YAML['server']['id']))
        print('[node1] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/scripts/build.sh'.format(CONF_YAML['node1']['id']))
        print('[node2] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/scripts/build.sh'.format(CONF_YAML['node2']['id']))
        Files.Clear()

    @staticmethod
    def Snapshot(name):
        print('[all] \t\t Taking snapshots of containers... ({})'.format(name))
        Tools.Call('pct snapshot {} server_{}'.format(CONF_YAML['server']['id'],name)) 
        Tools.Call('pct snapshot {} node1_{}'.format(CONF_YAML['node1']['id'],name)) 
        Tools.Call('pct snapshot {} node2_{}'.format(CONF_YAML['node2']['id'],name)) 
    
    @staticmethod
    def Rollback(name):
        print('[all] \t\t Rolling back containers... ({})'.format(name))
        Containers.Stop()
        Tools.Call('pct rollback {} server_{}'.format(CONF_YAML['server']['id'],name)) 
        Tools.Call('pct rollback {} node1_{}'.format(CONF_YAML['node1']['id'],name)) 
        Tools.Call('pct rollback {} node2_{}'.format(CONF_YAML['node2']['id'],name)) 
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Containers.Start()
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Services.Start()

class Files:
    @staticmethod
    def Generate():
        # Generate TEMP directory
        if os.path.exists(CONF_TEMP_PATH):
            shutil.rmtree(CONF_TEMP_PATH)
        pathlib.Path(CONF_TEMP_PATH).mkdir(parents=True, exist_ok=True)

        # lib
        shutil.copyfile(CONF_RES_PATH+"/libraries/controller.py", CONF_TEMP_PATH+"/controller.py")

        # Copy files related to SERVER into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/server/scripts/start.sh", CONF_TEMP_PATH+"/server_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/server/scripts/stop.sh", CONF_TEMP_PATH+"/server_stop.sh")
        shutil.copyfile(CONF_RES_PATH+"/server/scripts/build.sh", CONF_TEMP_PATH+"/server_build.sh")
        shutil.copyfile(CONF_RES_PATH+"/server/config/database.sql", CONF_TEMP_PATH+"/server_database.sql")
        shutil.copyfile(CONF_RES_PATH+"/server/config/args.yaml", CONF_TEMP_PATH+"/server_args.yaml")
        shutil.copyfile(CONF_RES_PATH+"/server/config/plugin.yaml", CONF_TEMP_PATH+"/server_plugin.yaml")
        shutil.copyfile(CONF_RES_PATH+"/server/config/redis.conf", CONF_TEMP_PATH+"/server_redis.conf")
        shutil.copyfile(CONF_RES_PATH+"/server/app.py", CONF_TEMP_PATH+"/server_app.py")

        # Copy files related to NODE1 into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/start.sh", CONF_TEMP_PATH+"/node1_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/stop.sh", CONF_TEMP_PATH+"/node1_stop.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/build.sh", CONF_TEMP_PATH+"/node1_build.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/config/args.yaml", CONF_TEMP_PATH+"/node1_args.yaml")
        shutil.copyfile(CONF_RES_PATH+"/client/config/plugin.yaml", CONF_TEMP_PATH+"/node1_plugin.yaml")
        shutil.copyfile(CONF_RES_PATH+"/client/config/redis.conf", CONF_TEMP_PATH+"/node1_redis.conf")
        shutil.copyfile(CONF_RES_PATH+"/client/app.py", CONF_TEMP_PATH+"/node1_app.py")

        # Copy files related to NODE2 into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/start.sh", CONF_TEMP_PATH+"/node2_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/stop.sh", CONF_TEMP_PATH+"/node2_stop.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/scripts/build.sh", CONF_TEMP_PATH+"/node2_build.sh")
        shutil.copyfile(CONF_RES_PATH+"/client/config/args.yaml", CONF_TEMP_PATH+"/node2_args.yaml")
        shutil.copyfile(CONF_RES_PATH+"/client/config/plugin.yaml", CONF_TEMP_PATH+"/node2_plugin.yaml")
        shutil.copyfile(CONF_RES_PATH+"/client/config/redis.conf", CONF_TEMP_PATH+"/node2_redis.conf")
        shutil.copyfile(CONF_RES_PATH+"/client/app.py", CONF_TEMP_PATH+"/node2_app.py")

    @staticmethod
    def Render():
        # Replace values LIB
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/controller.py","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/controller.py","%db_user%",str(CONF_YAML['server']['db_user']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/controller.py","%db_pass%",str(CONF_YAML['server']['db_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/controller.py","%db_name%",str(CONF_YAML['server']['db_name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/controller.py","%port_ui%",str(CONF_YAML['node2']['port_ui']))

        # Replace values in files related to SERVER
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%id%",str(CONF_YAML['server']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%port_ledger%",str(CONF_YAML['server']['port_ledger']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%name%",str(CONF_YAML['server']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%port_ui%",str(CONF_YAML['server']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%log_acapy%",str(CONF_YAML['server']['log_acapy']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%log_redis%",str(CONF_YAML['server']['log_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%log_indy%",str(CONF_YAML['server']['log_indy']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%log_tails%",str(CONF_YAML['server']['log_tails']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%log_web%",str(CONF_YAML['server']['log_web']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_build.sh","%db_user%",str(CONF_YAML['server']['db_user']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_build.sh","%db_pass%",str(CONF_YAML['server']['db_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%db_name%",str(CONF_YAML['server']['db_name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_id%",str(CONF_YAML['server']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_name%",str(CONF_YAML['server']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_ui_port%",str(CONF_YAML['server']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_acapy_port_1%",str(CONF_YAML['server']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_acapy_port_2%",str(CONF_YAML['server']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%server_ledger_port%",str(CONF_YAML['server']['port_ledger']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_id%",str(CONF_YAML['node1']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_name%",str(CONF_YAML['node1']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_ip%",str(CONF_YAML['node1']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_ui_port%",str(CONF_YAML['node1']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_acapy_port_1%",str(CONF_YAML['node1']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node1_acapy_port_2%",str(CONF_YAML['node1']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_id%",str(CONF_YAML['node2']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_name%",str(CONF_YAML['node2']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_ip%",str(CONF_YAML['node2']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_ui_port%",str(CONF_YAML['node2']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_acapy_port_1%",str(CONF_YAML['node2']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_database.sql","%node2_acapy_port_2%",str(CONF_YAML['node2']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_redis.conf","%port_redis%",str(CONF_YAML['server']['port_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%name%",str(CONF_YAML['server']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%port_acapy_1%",str(CONF_YAML['server']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%port_acapy_2%",str(CONF_YAML['server']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%port_tails%",str(CONF_YAML['server']['port_tails']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_args.yaml","%port_ledger%",str(CONF_YAML['server']['port_ledger']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_plugin.yaml","%port_redis%",str(CONF_YAML['server']['port_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_plugin.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))


        # Replace values in files related to Node 1
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%id%",str(CONF_YAML['node1']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%port_ui%",str(CONF_YAML['node1']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%log_acapy%",str(CONF_YAML['node1']['log_acapy']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%log_redis%",str(CONF_YAML['node1']['log_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%log_web%",str(CONF_YAML['node1']['log_web']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%name%",str(CONF_YAML['node1']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%port_acapy_1%",str(CONF_YAML['node1']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%port_acapy_2%",str(CONF_YAML['node1']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%port_tails%",str(CONF_YAML['node1']['port_tails']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%port_ledger%",str(CONF_YAML['server']['port_ledger']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_plugin.yaml","%port_redis%",str(CONF_YAML['node1']['port_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_plugin.yaml","%network_ip%",str(CONF_YAML['node1']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_redis.conf","%port_redis%",str(CONF_YAML['node1']['port_redis']))

        # Replace values in files related to Node 2
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%id%",str(CONF_YAML['node2']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%port_ui%",str(CONF_YAML['node2']['port_ui']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%log_acapy%",str(CONF_YAML['node2']['log_acapy']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%log_redis%",str(CONF_YAML['node2']['log_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%log_web%",str(CONF_YAML['node2']['log_web']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%name%",str(CONF_YAML['node2']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%port_acapy_1%",str(CONF_YAML['node2']['port_acapy_1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%port_acapy_2%",str(CONF_YAML['node2']['port_acapy_2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%port_tails%",str(CONF_YAML['node2']['port_tails']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%port_ledger%",str(CONF_YAML['server']['port_ledger']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_plugin.yaml","%port_redis%",str(CONF_YAML['node2']['port_redis']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_plugin.yaml","%network_ip%",str(CONF_YAML['node2']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_redis.conf","%port_redis%",str(CONF_YAML['node2']['port_redis']))

    @staticmethod
    def Push():
        print('[all] \t\t Pushing files...')
        # Push files to SERVER
        Tools.Call('pct exec {} -- mkdir /root/scripts'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- mkdir /root/config'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- mkdir /root/view'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- mkdir /root/logs'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- mkdir /root/cache'.format(CONF_YAML['server']['id']))
        Tools.Call('pct push {} {}/server_start.sh /root/scripts/start.sh'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_stop.sh /root/scripts/stop.sh'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_build.sh /root/scripts/build.sh'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_database.sql /root/config/database.sql'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/controller.py /root/controller.py'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_app.py /root/app.py'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_redis.conf /root/config/redis.conf'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_args.yaml /root/config/args.yaml'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_plugin.yaml /root/config/plugin.yaml'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server/view/home.html /root/view/home.html'.format(CONF_YAML['server']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/server/view/products.html /root/view/products.html'.format(CONF_YAML['server']['id'],CONF_RES_PATH))

        
        
        # Push files to NODE 1
        Tools.Call('pct exec {} -- mkdir /root/scripts'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- mkdir /root/config'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- mkdir /root/view'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- mkdir /root/logs'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- mkdir /root/cache'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct push {} {}/node1_start.sh /root/scripts/start.sh'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_stop.sh /root/scripts/stop.sh'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_build.sh /root/scripts/build.sh'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_args.yaml /root/config/args.yaml'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_plugin.yaml /root/config/plugin.yaml'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_redis.conf /root/config/redis.conf'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/controller.py /root/controller.py'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_app.py /root/app.py'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/client/view/home.html /root/view/home.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/client/view/products.html /root/view/products.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/client/view/supplychain.html /root/view/supplychain.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))

        

        # Push files to NODE 2
        Tools.Call('pct exec {} -- mkdir /root/scripts'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct exec {} -- mkdir /root/config'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct exec {} -- mkdir /root/view'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct exec {} -- mkdir /root/logs'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct exec {} -- mkdir /root/cache'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct push {} {}/node2_start.sh /root/scripts/start.sh'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_stop.sh /root/scripts/stop.sh'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_build.sh /root/scripts/build.sh'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_args.yaml /root/config/args.yaml'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_plugin.yaml /root/config/plugin.yaml'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_redis.conf /root/config/redis.conf'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/controller.py /root/controller.py'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_app.py /root/app.py'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/client/view/home.html /root/view/home.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/client/view/products.html /root/view/products.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/client/view/supplychain.html /root/view/supplychain.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))

        

        shutil.rmtree(CONF_TEMP_PATH)

    @staticmethod
    def Purge():
        print('[all] \t\t Purging files...')
        Tools.Call('pct exec {} -- bash -c "rm -rf /root/*"'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- bash -c "rm -rf /root/*"'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- bash -c "rm -rf /root/*"'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Clear():
        print('[all] \t\t Cleaning files...')
        Tools.Call('pct exec {} -- bash -c "rm /root/scripts/build.sh"'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- bash -c "rm /root/config/database.sql"'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- bash -c "rm /root/scripts/build.sh"'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- bash -c "rm /root/scripts/build.sh"'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Update():
        Services.Stop()
        Files.Purge()
        Files.Generate()
        Files.Render()
        Files.Push()

class Services:
    @staticmethod
    def Start():
        print('[all] \t\t Starting services...')
        Tools.SetSSH()
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh indy\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh tails\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh redis\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh redis\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node1']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh redis\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node2']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('pct exec {} -- bash -c "redis-cli --cluster create {}:{} {}:{} {}:{} --cluster-yes"'.format(CONF_YAML['server']['id'],CONF_YAML['server']['network_ip'],CONF_YAML['server']['port_redis'],CONF_YAML['node1']['network_ip'],CONF_YAML['node1']['port_redis'],CONF_YAML['node2']['network_ip'],CONF_YAML['node2']['port_redis']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh aries\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh aries\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node1']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh aries\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node2']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh app\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh app\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node1']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/scripts/start.sh app\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node2']['network_ip']))
        time.sleep(CONF_YAML['manage']['step_sleep'])

    @staticmethod
    def Stop():
        print('[all] \t\t Stopping services...')
        Tools.Call('pct exec {} -- bash /root/stop.sh'.format(CONF_YAML['server']['id']))
        Tools.Call('pct exec {} -- bash /root/stop.sh'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct exec {} -- bash /root/stop.sh'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Restart():
        print('[all] \t\t Restarting services...')
        Services.Stop()
        time.sleep(CONF_YAML['manage']['step_sleep'])
        Services.Start()

def AIO():
    datetime_start = datetime.datetime.now()
    Containers.Destroy()
    Containers.Create()
    Files.Generate()
    Files.Render()
    Files.Push()
    Containers.Build()
    Containers.Snapshot("build")
    Services.Start()
    Containers.Reboot()
    Services.Start()
    Containers.Snapshot("final")
    datetime_end = datetime.datetime.now()
    duration = round((datetime_end - datetime_start).total_seconds() / 60.0,1)
    print("\nBuild took {} minutes.".format(duration))
    print("\nEndpoints:")
    print("\t http://{}:{}".format(CONF_YAML['server']['network_ip'],CONF_YAML['server']['port_ui']))
    print("\t http://{}:{}".format(CONF_YAML['node1']['network_ip'],CONF_YAML['node1']['port_ui']))
    print("\t http://{}:{}".format(CONF_YAML['node2']['network_ip'],CONF_YAML['node2']['port_ui']))
    print()

if __name__ == "__main__":
    match " ".join(sys.argv[1:]):
        case "config":
            Tools.Config()
        case "build":
            AIO()
        case "update":
            Files.Update()
        case "start":
            Containers.Start()
            Services.Start()
        case "stop":
            Services.Stop()
            Containers.Stop()
        case "restart":
            Services.Restart()
        case "reboot":
            Containers.Reboot()
        case "help":
            Tools.Help()
        case "":
            Tools.Help()   
        case _:
            print(CONF_YAML['manage']['error_arg'])