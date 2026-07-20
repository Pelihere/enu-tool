import subprocess


class DNS_Enumeration:

    def __init__(self, target):
        self.target = target
        self.tool = None
        self.name_servers = []

    def version_enu(self):
        dnsVersionInfo = None
        try:
            dnsVersionInfo = subprocess.run(["dig", f"@{self.target}", "version.bind", "txt", "chaos"],
                                            capture_output=True, 
                                            text=True)
            self.tool = "dig"
            print("[+] running dif for version eumeration ...")
        except FileNotFoundError:
            self.tool = "nslookup"
            print("[*] dig is not installed! trying nslookup")
            dnsVersionInfo = subprocess.run(["nslookup", "-type=NS", self.target], 
                                            capture_output=True,
                                            text=True)
            
            print("[+] running nslookup for version enumeration")

        except Exception as e:
            print(f"[-] something went wrong while running dig. Error \n {e}")

        return dnsVersionInfo

    def name_server_enu(self):
        try:
            nameServerInfo = subprocess.run(["dig", "NS", self.target],
                                            capture_output=True,
                                            text=True)
            print("[+] running dig for name server enumeration ...")
        except FileNotFoundError:
            print("[-] dig is not installed !")
        except Exception as e:
            print(f"[-] something went wrong while running dig. Error \n {e}") 

        for line in nameServerInfo.stdout.splitlines():
            if " IN NS " in line:
                self.name_servers.append(line.split()[-1].rstrip("."))


        return nameServerInfo
    
    def soa_enu(self):
        if self.tool == 'dig':
            try:
                soaInfo = subprocess.run(["dig", "SOA", self.target],
                                        capture_output=True,
                                        text=True)
                print("[+] running dig for SOA enumeration ...")
            except Exception as e:
                print(f"something went wrong while running dig. Error \n {e}")
        elif self.tool == 'nslookup' :
            try:
                soaInfo = subprocess.run(["nslookup", "-type=SOA", self.target], 
                                         capture_output=True, 
                                         text=True)
            except Exception as e:
                print(f"something went wrong while running nslookup. Error \n {e}")        

        return soaInfo
    
    def zone_transfer_enu(self, nameServer):
        zoneTransferInfo = subprocess.run(["dig", "AXFR", self.target, f"@{nameServer}"],
                                            capture_output=True,
                                            text=True)
        
        return zoneTransferInfo
    
    def gen_enu(self):
        results = {}
        records = [
            'A','MX','TXT','CNAME','AAAA'
        ]

        for command in records :
            results[command] = subprocess.run(["dig", command, self.target], capture_output=True, text=True)

    def run(self):
        results = {}

        results["version"] = self.version_enu()
        results["name_servers"] = self.name_server_enu()
        results["soa"] = self.soa_enu()
        results["zone_transfer"] = {}
        for ns in self.name_servers:
            results["zone_transfer"][ns] = self.zone_transfer_enu(ns)

        results["records"] = self.gen_enu()

        return results