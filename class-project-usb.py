#! /usr/bin/env python

import json
import sys
from cli import *

def show_dev_version():
    ver_data = json.loads(clid('show version'))

    dev_ver = ver_data['kickstart_ver_str']
    dev_mod = ver_data['chassis_id']
    dev_boot_file = ver_data['kick_file_name']

    dev_ver_dict = { 'Version': dev_ver, 'Model': dev_mod, 'Bootfile': dev_boot_file }

    return dev_ver_dict

def check_version():
    desired_9k_ver = 'nxos.7.1.3.1.bin'
    desired_6k_ver = 'nxos.7.0.3.I3.1.bin'
    
    current_ver_data = show_dev_version()
    current_ver_raw = current_ver_data['Bootfile']
    current_ver = current_ver_raw.strip('bootflash:///')

    current_model_raw = current_ver_data['Model']
    current_model = current_model_raw.split(' ')[0]

#    current_model = 'Nexus6000'

    if desired_6k_ver == current_ver and current_model == 'Nexus6000':
        print 'Current 6K version is acceptable, moving to next step.'
        upgrade_check = False
    elif desired_6k_ver != current_ver and current_model =='Nexus6000':
        print 'Current 6K version requires upgrading, beginning version upgrade process.'
        upgrade_check = True
    elif desired_9k_ver == current_ver and current_model == 'Nexus9000':
        print 'Current 9K version is acceptable, moving to next step.'
        upgrade_check = False
    elif desired_9k_ver != current_ver and current_model == 'Nexus9000':
        print 'Current 9K version requires upgrading, beginning version upgrade process.'
        upgrade_check = True

    if upgrade_check == True:
        try:
            cli('copy bootflash:/testcode/imagetest.bin bootflash:imagetest.bin')
            print 'Copying System Image...'
        except:
            print 'Oh Poop! Something went wrong, probably Brents fault'
            exit(0)

def copy_config():
    command = len(sys.argv)
    args = sys.argv

    if  command == 1:
        print '\n Script requires the device config file name. \n\n '
        print '\n Please include the desired router configuration file.'
    else:
        print "Good to go"

    if command == 1:
        args1 = raw_input("> Please enter the text file: ")
        args.append(args1)
    
    print 'Copying configuration to running-config... '
    copy = cli('copy bootflash:/testcode/%s running-config'%args[1])
    print 'Copy complete.'

    return copy_config

def set_bootvar():
    boot = cli('config t ; boot nxos bootflash:/imagetest.bin ; end')

    print 'Setting boot variable to NXOS Image.... '
    print 'Saving configuration...'
    save = cli('copy run start')

    print 'Save complete.'

    return set_bootvar

def main():

    ver = show_dev_version()

    print json.dumps(ver, indent=4)

    ver_check = check_version()

    conf = copy_config()
    bootvar = set_bootvar()

if __name__ == "__main__":
    main()