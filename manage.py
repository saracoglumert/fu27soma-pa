#!/usr/bin/python3
from subprocess import call
import yaml

with open('conf.yaml', 'r') as file:
    conf = yaml.safe_load(file)

def init():
    call('if ! test -f {}; then wget {} -O ${} fi'.format(conf['template']['path'],conf['template']['url'],conf['template']['path']),shell=True)
    call('apt install sshpass -y',shell=True)
    call('mkdir temp',shell=True)

def build():
    build_create()
    
    build_push_init()
    build_run_init()
    
    build_generate_args()
    build_push_args()
    
    build_generate_start()
    build_push_start()

    build_clear()

def build_create():
    call('pct create {} {} --hostname "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,gw={},ip={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
        conf['server']['id'],
        conf['template']['path'],
        conf['server']['hostname'],
        conf['conf']['memory'],
        conf['conf']['gateway'],
        conf['server']['ip']+'/24',
        conf['conf']['disk'],
        conf['conf']['passwd'],
        conf['conf']['ssh']
    ),shell=True)
    call('pct create {} {} --hostname "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,gw={},ip={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
        conf['node1']['id'],
        conf['template']['path'],
        conf['node1']['hostname'],
        conf['conf']['memory'],
        conf['conf']['gateway'],
        conf['node1']['ip']+'/24',
        conf['conf']['disk'],
        conf['conf']['passwd'],
        conf['conf']['ssh']
    ),shell=True)
    call('pct create {} {} --hostname "{}" --memory "{}" --net0 name=eth0,bridge=vmbr0,firewall=1,gw={},ip={},type=veth --storage local-lvm --rootfs local-lvm:{} --unprivileged 1 --ignore-unpack-errors --ostype debian --password={} --start 1 --ssh-public-keys {} --features nesting=1'.format(
        conf['node2']['id'],
        conf['template']['path'],
        conf['node2']['hostname'],
        conf['conf']['memory'],
        conf['conf']['gateway'],
        conf['node2']['ip']+'/24',
        conf['conf']['disk'],
        conf['conf']['passwd'],
        conf['conf']['ssh']
    ),shell=True)

def build_push_init():
    call('pct push {} ~/fu27soma-project/res/init/server.sh ~/init.sh'.format(conf['server']['id']),shell=True)
    call('pct push {} ~/fu27soma-project/res/init/node.sh ~/init.sh'.format(conf['node1']['id']),shell=True)
    call('pct push {} ~/fu27soma-project/res/init/node.sh ~/init.sh'.format(conf['node2']['id']),shell=True)

def build_run_init():
    call('pct exec {} -- bash ~/init.sh'.format(conf['server']['id']),shell=True)
    call('pct exec {} -- bash ~/init.sh'.format(conf['node1']['id']),shell=True)
    call('pct exec {} -- bash ~/init.sh'.format(conf['node2']['id']),shell=True)

def build_generate_args():
    # Read in the file
    with open('res/args/node.yaml', 'r') as file:
        node1 = file.read()
    with open('res/args/node.yaml', 'r') as file:
        node2 = file.read()
    
    # Replace the target string
    node1 = node1.replace('%hostname%', conf['node1']['hostname']).replace('%endpoint%', str(conf['node1']['endpoint'])).replace('%admin%', str(conf['node1']['admin'])).replace('%server_endpoint%', str(conf['server']['endpoint'])).replace('%server_ip%', str(conf['server']['ip'])).replace('%tails%', str(conf['conf']['tails']))
    node2 = node2.replace('%hostname%', conf['node2']['hostname']).replace('%endpoint%', str(conf['node2']['endpoint'])).replace('%admin%', str(conf['node2']['admin'])).replace('%server_endpoint%', str(conf['server']['endpoint'])).replace('%server_ip%', str(conf['server']['ip'])).replace('%tails%', str(conf['conf']['tails']))

    # Write the file out again
    with open('temp/node1.yaml', 'w') as file:
        file.write(node1)

    with open('temp/node2.yaml', 'w') as file:
        file.write(node2)

def build_push_args():
    call('pct push {} ~/fu27soma-project/temp/node1.yaml ~/args.yaml'.format(conf['node1']['id']),shell=True)
    call('pct push {} ~/fu27soma-project/temp/node2.yaml ~/args.yaml'.format(conf['node2']['id']),shell=True)

def build_generate_start():
    with open('res/start/server.sh', 'r') as file:
        data = file.read()
    
    data = data.replace('%server_ip%',str(conf['server']['ip'])).replace('%server_endpoint%',str(conf['server']['endpoint'])).replace('%server_ledger',conf['server']['ledger'])

    with open('temp/start_server.sh', 'w') as file:
        file.write(data)

def build_push_start():
    call('pct push {} ~/fu27soma-project/temp/start_server.sh ~/start.sh'.format(conf['server']['id']),shell=True)
    call('pct push {} ~/fu27soma-project/res/start/node.sh ~/start.sh'.format(conf['node1']['id']),shell=True)
    call('pct push {} ~/fu27soma-project/res/start/node.sh ~/start.sh'.format(conf['node2']['id']),shell=True)

def build_clear():
    call('rm -r temp',shell=True)   

def start():
    start_containers()
    start_ssh()

def start_containers():
    call('pct start {}'.format(conf['server']['id']),shell=True)
    call('pct start {}'.format(conf['node1']['id']),shell=True)
    call('pct start {}'.format(conf['node2']['id']),shell=True)

def start_ssh():
    call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(conf['conf']['ssh'],conf['server']['ip']),shell=True)
    call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(conf['conf']['ssh'],conf['node1']['ip']),shell=True)
    call('ssh-keygen -f "{}" -R "{}"] > /dev/null 2>&1'.format(conf['conf']['ssh'],conf['node2']['ip']),shell=True)
    call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash ~/start.sh\''.format(conf['conf']['passwd'],conf['server']['ip']),shell=True)
    call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash ~/start.sh\''.format(conf['conf']['passwd'],conf['node1']['ip']),shell=True)
    call('sshpass -p {} ssh -oStrictHostKeyChecking=no root@{} \'bash ~/start.sh\''.format(conf['conf']['passwd'],conf['node2']['ip']),shell=True)

def stop():
    call('pct stop {}'.format(conf['server']['id']),shell=True)
    call('pct stop {}'.format(conf['node1']['id']),shell=True)
    call('pct stop {}'.format(conf['node2']['id']),shell=True)

def destroy():
    stop()
    call('pct destroy {}'.format(conf['server']['id']),shell=True)
    call('pct destroy {}'.format(conf['node1']['id']),shell=True)
    call('pct destroy {}'.format(conf['node2']['id']),shell=True)