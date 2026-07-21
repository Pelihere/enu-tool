import subprocess

class NTP_Enumeration:
    def __init__(self, target):
        self.target = target

    def version_enu(self):
        verInfo = None
        try:
            verInfo = subprocess.run(["ntpq", "-c", "rv", self.target], 
                                     capture_output=True,
                                     text=True)

            print("[+] running ntpq for version detection ...")
        except FileNotFoundError:
            print("[-] ntpq is not installed !")
        except Exception as e:
            print(f"something went wrong while running ntpq. Error: \n {e}")

        return verInfo
    
    def peer_enu(self):
        peerInfo = None
        try:
            peerInfo = subprocess.run(["ntpq", "-c", "peers", self.target], 
                                      capture_output=True,
                                      text=True)
            print("[+] running ntpq for peer enumeration ...")
        

        except Exception as e:
            print(f"[-] something went wrong while running ntpq. Error: \n {e} ")
        
        return peerInfo

    def system_valriables_enu(self):
        sysValInfo = None
        try:
            sysValInfo = subprocess.run(["ntpq", "-c", "readvar", self.target], 
                                        capture_output=True, 
                                        text=True)
            print("[+] running ntpq for system variables detection ...")
        except Exception as e:
            print(f"[-] something went wrong while running ntpq. Error: \n {e} ")
        
        return sysValInfo
    
    def monlist_enu(self):
        monlistInfo = None
        try:
            monlistInfo = subprocess.run(["ntpq", "-c", "monlist", self.target],
                                         capture_output=True,
                                         text=True)

            print("[+] running ntpq for Monlist enumeration ...")

        except Exception as e:
            print(f"[-] something went wrong while running ntpq. Error: \n {e} ")

        return monlistInfo

    def sysinfo_enu(self):
        sysInfo = None
        try:
            sysInfo = subprocess.run(["ntpq", "-c", "sysinfo", self.target],
                                     capture_output=True,
                                     text=True)        
            
            print("[+] running ntpq ...")

        except Exception as e:
            print(f"[-] something went wrong while running ntpq. Error: \n {e} ")
        
        return sysInfo
    
    def run(self):
        results = {}


        results["version"] = self.version_enu()
        results["Peer"] = self.peer_enu()
        results["SysVal"] = self.system_valriables_enu()
        results["Monlist"] = self.monlist_enu()
        results["SysInfo"] = self.sysinfo_enu()

        return results