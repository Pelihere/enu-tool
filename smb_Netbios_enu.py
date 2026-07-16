import subprocess
import platform

class Enumeration:

    def __init__(self, target):
        self.target = target
        self.os = platform.system().lower()

    def service_name_scan(self):
        try:
            if self.os == "linux":
                name_services = subprocess.run(["nmblookup", "-A", self.target],
                                                capture_output=True,
                                                text=True)
                print("nmlookup is running ...")
            elif self.os == "windows":
                name_services = subprocess.run(["nbtstat", "-A", self.target], 
                                                capture_output=True,
                                                text=True)
                print("nbstat is running ...")

        except FileNotFoundError:
            print("some off the requiered tools are missing")
        except Exception as e:
            print(f"something gone wrong, Error : \n {e}")

        return {
            "tool": "nbtstat",
            "success": True,
            "stdout": name_services.stdout,
            "stderr": name_services.stderr,
            "returncode": 0
        }
    
    def smb_scan(self):
        try:
            smb_res = subprocess.run(["smbclient","-L", f"//{self.target}", "-N"],
                                       capture_output=True, 
                                       text=True)
            print("smbcleint is running ...")
        except FileNotFoundError:
            print("some requiered tools are missing")
        
        except Exception as e:
            print(f"something gone wrong, Error : \n {e}")
            
        return {
            "tool": "smbclient",
            "success": True,
            "stdout": smb_res.stdout,
            "stderr": smb_res.stderr,
            "returncode": 0
        }
    
    def rpc_enumeration(self):
        results = {}
        commands = [
            "lsaquery",
            "enumdomusers",
            "enumdomgroups",
            "querydispinfo"
        ]

        for conmmand in commands:
            res = subprocess.run(
                [
                    "rpcclient",
                    "-U", "",
                    "-N",
                    self.target,
                    "-c",
                    conmmand
                ],
                capture_output=True,
                text=True
            )

            results[conmmand] = res.stdout