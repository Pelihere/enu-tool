import subprocess


class IPsec_Enumeration:

    def __init__(self, target):
        self.target = target


    def IKE_walker(self, command):
        commandres = None
        try:
            commandres = subprocess.run(["ike-scan", command, self.target],
                                      capture_output=True,
                                       text=True)
            
            print("[+] running ike-scan ... ")

        except FileNotFoundError:
            print("[-] ike-scan is not installed !")
        except Exception as e:
            print(f"[-] something went wrong while running ike-scan. Error: \n {e}")

        return commandres
    

    def IKE_enu(self):
        IKEInfo = None
        try:
            IKEInfo = subprocess.run(["ike-scan", self.target],
                                      capture_output=True,
                                       text=True)
            
            print("[+] running ike-scan for IKE enumeration ... ")

        except FileNotFoundError:
            print("[-] ike-scan is not installed !")
        except Exception as e:
            print(f"[-] something went wrong while running ike-scan. Error: \n {e}")

        return IKEInfo
    

    
    def fingerprinting_enu(self):
        return self.IKE_walker("--multiline")

    def aggressive_mode_enu(self):
        return self.IKE_walker("--aggressive")
    
    def ike_version_enu(self):
        IVInfo = None
        try:
            IVInfo = subprocess.run(["nmap", "-sU", "-p500", "--script", "ike-version", self.target], 
                                    capture_output=True, 
                                    text=True)
            
            print("[+] running nmap for ike version enumeration ...")

        except FileNotFoundError:
            print("[-] namp is not installed !")
        except Exception as e:
            print(f"[-] soemthing went wrong while running nmap. Error: \n {e}")

        return IVInfo
    

    def run(self):
        results = {}

        results["ike"] = self.IKE_enu()
        results["fingerprint"] = self.fingerprinting_enu()
        results["aggressive_mode"] = self.aggressive_mode_enu()
        results["ike_version"] = self.ike_version_enu()

        return results