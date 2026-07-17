from port_scanner import port_scan
from smb_Netbios_enu import Enumeration as SNE
from validators import ipv4, domain



ports = {
    "netbios udp" : 137,
    "netbios tcp" : [139, 445],
    "snmp queries" : 161,
    "snmp traps" : 162
}


def get_basec_info():
    target = input("[+] Enter target to scan : ")
    if (ipv4(target) or domain(target)):
        openPorts = port_scan.scan(target=target)

    return openPorts

def enumerationn_performer():
    pass