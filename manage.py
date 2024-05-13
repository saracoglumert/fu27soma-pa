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
        if os.path.exists(CONF_YAML['host']['container_template_path']):
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
        print("./manage build \t\t Build containers")
        print("./manage start \t\t Start containers")
        print("./manage stop \t\t Stop containers")
        print("./manage destroy \t Destroy containers")
        print("./manage config \t Runs configuration script")
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

class Containers:
    @staticmethod
    def Create():
        # Check for template
        Tools.Template()
        
        # Create containers
        print('[server] \t Creating container...')
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
            CONF_YAML['host']['ssh']))
        print('[node1] \t Creating container...')
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
            CONF_YAML['host']['ssh']))
        print('[node2] \t Creating container...')
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
            CONF_YAML['host']['ssh']))

    @staticmethod
    def Start():
        print('[all] \t Starting containers...')
        Tools.Call('pct start {}'.format(CONF_YAML['server']['id']))
        Tools.Call('pct start {}'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct start {}'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Reboot():
        print('[all] \t Rebooting containers...')
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

class Files:
    @staticmethod
    def Generate():
        print('[all] \t\t Generating files...')
        # Generate TEMP directory
        if os.path.exists(CONF_TEMP_PATH):
            shutil.rmtree(CONF_TEMP_PATH)
        pathlib.Path(CONF_TEMP_PATH).mkdir(parents=True, exist_ok=True)
        
        # Copy files related to SERVER into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/server/start.sh", CONF_TEMP_PATH+"/server_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/server/init.sh", CONF_TEMP_PATH+"/server_init.sh")
        shutil.copyfile(CONF_RES_PATH+"/server/db.sql", CONF_TEMP_PATH+"/server_db.sql")

        # Copy files related to NODE1 into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/node/start.sh", CONF_TEMP_PATH+"/node1_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/node/init.sh", CONF_TEMP_PATH+"/node1_init.sh")
        shutil.copyfile(CONF_RES_PATH+"/node/args.yaml", CONF_TEMP_PATH+"/node1_args.yaml")
        shutil.copyfile(CONF_RES_PATH+"/node/plugin.yaml", CONF_TEMP_PATH+"/node1_plugin.yaml")
        shutil.copyfile(CONF_RES_PATH+"/node/web.py", CONF_TEMP_PATH+"/node1_web.py")

        # Copy files related to NODE2 into TEMP directory
        shutil.copyfile(CONF_RES_PATH+"/node/start.sh", CONF_TEMP_PATH+"/node2_start.sh")
        shutil.copyfile(CONF_RES_PATH+"/node/init.sh", CONF_TEMP_PATH+"/node2_init.sh")
        shutil.copyfile(CONF_RES_PATH+"/node/args.yaml", CONF_TEMP_PATH+"/node2_args.yaml")
        shutil.copyfile(CONF_RES_PATH+"/node/plugin.yaml", CONF_TEMP_PATH+"/node2_plugin.yaml")
        shutil.copyfile(CONF_RES_PATH+"/node/web.py", CONF_TEMP_PATH+"/node2_web.py")

    @staticmethod
    def Render():
        print('[all] \t\t Rendering files...')
        # Replace values in files related to SERVER
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%ledger_endpoint%",str(CONF_YAML['server']['ledger_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_start.sh","%ledger_name%",str(CONF_YAML['server']['ledger_name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_init.sh","%db_user%",str(CONF_YAML['server']['db_user']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_init.sh","%db_pass%",str(CONF_YAML['server']['db_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_db.sql","%db_name%",str(CONF_YAML['server']['db_name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_db.sql","%node1_id%",str(CONF_YAML['node1']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_db.sql","%node2_id%",str(CONF_YAML['node2']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_db.sql","%node1_name%",str(CONF_YAML['node1']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/server_db.sql","%node2_name%",str(CONF_YAML['node2']['name']))

        # Replace values in files related to Node 1
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_start.sh","%id%",str(CONF_YAML['node1']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_init.sh","%redis_pass%",str(CONF_YAML['node1']['redis_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%name%",str(CONF_YAML['node1']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%acapy_endpoint1%",str(CONF_YAML['node1']['acapy_endpoint1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%acapy_endpoint2%",str(CONF_YAML['node1']['acapy_endpoint2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%tails_endpoint%",str(CONF_YAML['node1']['tails_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_args.yaml","%ledger_endpoint%",str(CONF_YAML['server']['ledger_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_plugin.yaml","%redis_endpoint%",str(CONF_YAML['node1']['redis_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_plugin.yaml","%redis_pass%",str(CONF_YAML['node1']['redis_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_plugin.yaml","%network_ip%",str(CONF_YAML['node1']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_web.py","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_web.py","%db_user%",str(CONF_YAML['server']['db_user']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_web.py","%db_pass%",str(CONF_YAML['server']['db_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node1_web.py","%db_name%",str(CONF_YAML['server']['db_name']))

        # Replace values in files related to Node 2
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_start.sh","%id%",str(CONF_YAML['node2']['id']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_init.sh","%redis_pass%",str(CONF_YAML['node2']['redis_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%name%",str(CONF_YAML['node2']['name']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%acapy_endpoint1%",str(CONF_YAML['node2']['acapy_endpoint1']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%acapy_endpoint2%",str(CONF_YAML['node2']['acapy_endpoint2']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%tails_endpoint%",str(CONF_YAML['node2']['tails_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_args.yaml","%ledger_endpoint%",str(CONF_YAML['server']['ledger_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_plugin.yaml","%redis_endpoint%",str(CONF_YAML['node2']['redis_endpoint']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_plugin.yaml","%redis_pass%",str(CONF_YAML['node2']['redis_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_plugin.yaml","%network_ip%",str(CONF_YAML['node2']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_web.py","%network_ip%",str(CONF_YAML['server']['network_ip']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_web.py","%db_user%",str(CONF_YAML['server']['db_user']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_web.py","%db_pass%",str(CONF_YAML['server']['db_pass']))
        Tools.ReplaceInplace(CONF_TEMP_PATH+"/node2_web.py","%db_name%",str(CONF_YAML['server']['db_name']))

    @staticmethod
    def Push():
        print('[all] \t\t Pushing files...')
        # Push files to SERVER
        Tools.Call('pct push {} {}/server_start.sh /root/start.sh'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_init.sh /root/init.sh'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/server_db.sql /root/db.sql'.format(CONF_YAML['server']['id'],CONF_TEMP_PATH))
        
        # Push files to NODE 1
        Tools.Call('pct push {} {}/node1_start.sh /root/start.sh'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_init.sh /root/init.sh'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_args.yaml /root/args.yaml'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_plugin.yaml /root/plugin.yaml'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node1_web.py /root/web.py'.format(CONF_YAML['node1']['id'],CONF_TEMP_PATH))
        Tools.Call('pct exec {} -- mkdir /root/templates'.format(CONF_YAML['node1']['id']))
        Tools.Call('pct push {} {}/node/templates/index.html /root/templates/index.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/node/templates/products.html /root/templates/products.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/node/templates/supplychain.html /root/templates/supplychain.html'.format(CONF_YAML['node1']['id'],CONF_RES_PATH))

        # Push files to NODE 2
        Tools.Call('pct push {} {}/node2_start.sh /root/start.sh'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_init.sh /root/init.sh'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_args.yaml /root/args.yaml'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_plugin.yaml /root/plugin.yaml'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct push {} {}/node2_web.py /root/web.py'.format(CONF_YAML['node2']['id'],CONF_TEMP_PATH))
        Tools.Call('pct exec {} -- mkdir /root/templates'.format(CONF_YAML['node2']['id']))
        Tools.Call('pct push {} {}/node/templates/index.html /root/templates/index.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/node/templates/products.html /root/templates/products.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))
        Tools.Call('pct push {} {}/node/templates/supplychain.html /root/templates/supplychain.html'.format(CONF_YAML['node2']['id'],CONF_RES_PATH))

        shutil.rmtree(CONF_TEMP_PATH)

class App:
    @staticmethod
    def Build():    
        print('[server] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/init.sh'.format(CONF_YAML['server']['id']))
        print('[node1] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/init.sh'.format(CONF_YAML['node1']['id']))
        print('[node2] \t Running build script...')
        Tools.Call('pct exec {} -- bash /root/init.sh'.format(CONF_YAML['node2']['id']))

    @staticmethod
    def Start():    
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh'],CONF_YAML['server']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh'],CONF_YAML['node1']['network_ip']))
        Tools.Call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(CONF_YAML['host']['ssh'],CONF_YAML['node2']['network_ip']))
        print('[server] \t Running start script...')
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/start.sh\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['server']['network_ip']))
        print('[node1] \t Running start script...')
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/start.sh\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node1']['network_ip']))
        print('[node2] \t Running start script...')
        Tools.Call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash /root/start.sh\''.format(CONF_YAML['host']['container_pass'],CONF_YAML['node2']['network_ip']))

def AIO():
    datetime_start = datetime.datetime.now()
    Containers.Destroy()
    Containers.Create()
    Files.Generate()
    Files.Render()
    Files.Push()
    App.Build()
    App.Start()
    datetime_end = datetime.datetime.now()
    duration = round((datetime_end - datetime_start).total_seconds() / 60.0,1)
    print("\nBuild took {} minutes.".format(duration))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
        match cmd:
            case "build":
                AIO()
            case "destroy":
                Containers.Destroy()
            case "start":
                Containers.Start()
                time.sleep(5)
                App.Start()
            case "stop":
                Containers.Stop()
            case "config":
                Tools.Config()
            case "help":
                Tools.Help()
            case _:
                print(CONF_YAML['manage']['error_arg'])
    elif len(sys.argv) == 1:
        Tools.Help()
    else:
        print(CONF_YAML['manage']['error_arg'])