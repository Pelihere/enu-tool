from port_scanner import port_scan
from smb_Netbios_enu import SMB_Netbios_Enumeration as SNE
from SNMP_enu import SNMP_Enumeration as SE
from LDAP_enu import LDAP_Enumeration as LE
from validators import ipv4, domain




def get_basec_info():
    target = input("[+] Enter target to scan : ")
    if (ipv4(target) or domain(target)):
        openPorts = port_scan.scan(target=target)

    return openPorts

def enumerationn_executer(ports):
    pass