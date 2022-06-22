#!/bin/python3

import time

import sys

# setup toolbar

toolbar_width = 40

BAR_width = 40

sys.stdout.write("[*] Starting mac_changer " + "[%s]" % (" " * BAR_width))

sys.stdout.flush()

sys.stdout.write("\b" * (BAR_width + 1))

for i in range(BAR_width):
    time.sleep(0.1)  # do real work here

    # update the bar

    sys.stdout.write(".")

    sys.stdout.flush()

sys.stdout.write("]\n")  # this ends the progress bar

print(' @@@@@@@@@@    @@@@@@    @@@@@@@                  @@@@@@@  @@@  @@@  ')

print(' @@@@@@@@@@@  @@@@@@@@  @@@@@@@@                 @@@@@@@@  @@@  @@@  ')

print(' @@! @@! @@!  @@!  @@@  !@@                      !@@       @@!  @@@  ')

print(' !@! !@! !@!  !@!  @!@  !@!                      !@!       !@!  @!@  ')

print('  @!! !!@ @!@  @!@!@!@!  !@!                      !@!       @!@!@!@! ')

print('  !@!   ! !@!  !!!@!!!!  !!!                      !!!       !!!@!!!! ')

print('  !!:     !!:  !!:  !!!  :!!                      :!!       !!:  !!! ')

print('  :!:     :!:  :!:  !:!  :!:                      :!:       :!:  !:! ')

print('  :::     ::   ::   :::   ::: :::  :::::::::::::   ::: :::  ::   ::: ')

print('   :      :     :   : :   :: :: :  :::::::::::::   :: :: :   :   : : ')

print('  @@@@@@   @@@  @@@   @@@@@@@@  @@@@@@@@  @@@@@@@   ')

print('  @@@@@@@@  @@@@ @@@  @@@@@@@@@  @@@@@@@@  @@@@@@@@  ')

print('  @@!  @@@  @@!@!@@@  !@@        @@!       @@!  @@@  ')

print('  !@!  @!@  !@!!@!@!  !@!        !@!       !@!  @!@  ')

print('  @!@!@!@!  @!@ !!@!  !@! @!@!@  @!!!:!    @!@!!@!   ')

print('  !!!@!!!!  !@!  !!!  !!! !!@!!  !!!!!:    !!@!@!    ')

print('  !!:  !!!  !!:  !!!  :!!   !!:  !!:       !!: :!!   ')

print('  :!:  !:!  :!:  !:!  :!:   !::  :!:       :!:  !:!  ')

print('  ::   :::   ::   ::   ::: ::::   :: ::::  ::   :::  ')

print('  :   : :  ::    :    :: :: :   : :: ::    :   : :  ')

# importing modules

import subprocess

import optparse

import re


# getting arguments from user

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--Interface", dest="interface", help="Interface for Changing Mac address")

    parser.add_option("-m", "--Mac", dest="new_mac", help="New MAc address")

    (options, arguments) = parser.parse_args()

    if not options.interface:

        parser.error("[-] Please specify an interface to continue, use --help for more info")

    elif not options.new_mac:

        parser.error("[-] Please specify a New Mac to continue, use --help for more info")

    return options


# here is where the mac address change

def change_mac(interface, new_mac):
    print("[+] Changing Mac address for " + interface + " to " + new_mac)

    subprocess.call(["sudo", "ifconfig", interface, "down"])

    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])

    subprocess.call(["sudo", "ifconfig", interface, "up"])


# here is the mac_filtering in the ifconfig

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:

        return mac_address_search_result.group(0)

    else:

        print("[-] Sorry, could not read Mac Address")


options = get_arguments()

current_mac = get_current_mac(options.interface)

print("Current Mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:

    print("[+] Mac address was successfully changed to " + current_mac)

else:

    print("[-] MAc address did not changed")

