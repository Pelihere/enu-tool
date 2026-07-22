from port_scanner import port_scan
from smb_Netbios_enu import SMBNetBIOSEnumeration as SNE
from SNMP_enu import SNMPEnumeration as SE
from LDAP_enu import LDAPEnumeration as LE
from SMTP_enu import SMTPEnumeration as SME
from DNS_enu import DNSEnumeration as DE
from NTP_enu import NTP_Enumeration as NE
from IPsec_enu import IPsec_Enumeration as IE
from validators import ipv4, domain

enumeration_modules = {
    53: DE,
    123: NE,
    161: SE,
    389: LE,
    636: LE,
    25: SME,
    139: SNE,
    445: SNE,
    500: IE,
    4500: IE,
}

def get_basec_info():
    target = input("[+] Enter target to scan : ")
    if (ipv4(target) or domain(target)):
        openPorts = port_scan.scan(target=target)

    return openPorts

def enumerationn_executer(ports):
    pass


if __name__ == "__main__":
    enumerationn_executer(get_basec_info())