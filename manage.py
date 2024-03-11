#!/usr/bin/python3
from subprocess import call
import yaml

with open('conf.yml', 'r') as file:
    conf = yaml.safe_load(file)

def init():
    call('git clone https://github.com/bcgov/von-network',shell=True)
    call('if ! test -f $CONF_TEMPLATE_PATH; then; wget $CONF_TEMPLATE_URL -O $CONF_TEMPLATE_PATH; fi',shell=True)

def build():
    pass
init()