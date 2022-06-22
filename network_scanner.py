#!/usr/bin/env python3

#Python script to scan networks for IP and MAC addresses

import scapy.all as scapy
import optparse

# Function to get CLI arguments or return help info
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP range for network scan in /24 format.")
    (options, arguments) = parser.parse_args()
    if not options.target:
        print("network_scanner: try 'network_scanner.py --help' for more information")
        parser.exit()
    return options

# Function to scan network
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

# Function to print scan results
def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    if results_list:
        for client in results_list:
            print(client["ip"] + "\t\t" + client["mac"])
    else:
        print("No results found! No nodes on network or incorrect IP entered. Check target IP and try again.")

#MAIN
options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)