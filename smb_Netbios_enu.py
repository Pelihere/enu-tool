import subprocess
import platform

class SMB_Netbios_Enumeration:

    def __init__(self, target):
        self.target = target
        self.os = platform.system().lower()

    def service_name_scan(self):

        if self.os == "windows":
            tool = "nbtstat"
            command = ["nbtstat", "-A", self.target]

        elif self.os == "linux":
            tool = "nmblookup"
            command = ["nmblookup", "-A", self.target]

        else:
            print("Unsupported operating system")
            return None

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            print(f"{tool} is running ...")

        except FileNotFoundError:
            print(f"{tool} is not installed")
            return None

        except Exception as e:
            print(f"Something went wrong: {e}")
            return None

        return {
            "tool": tool,
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    def smb_scan(self):
        try:
            smb_res = subprocess.run(["smbclient","-L", f"//{self.target}", "-N"],
                                       capture_output=True, 
                                       text=True)
            print("smbcleint is running ...")
        except FileNotFoundError:
            print("smbclient is not installed")
        
        except Exception as e:
            print(f"something gone wrong, Error : \n {e}")
            
        return {
            "tool": "smbclient",
            "success": smb_res.returncode == 0,
            "stdout": smb_res.stdout,
            "stderr": smb_res.stderr,
            "returncode": smb_res.returncode
        }
    
    def rpc_enumeration(self):
        results = {}

        commands = [
            "lsaquery",
            "enumdomusers",
            "enumdomgroups",
            "querydispinfo"
        ]

        for command in commands:
            try:
                res = subprocess.run(
                    [
                        "rpcclient",
                        "-U", "",
                        "-N",
                        self.target,
                        "-c",
                        command
                    ],
                    capture_output=True,
                    text=True
                )

                results[command] = {
                    "success": res.returncode == 0,
                    "stdout": res.stdout,
                    "stderr": res.stderr,
                    "returncode": res.returncode
                }

            except FileNotFoundError:
                results[command] = {
                    "success": False,
                    "error": "rpcclient is not installed"
                }

            except Exception as e:
                results[command] = {
                    "success": False,
                    "error": str(e)
                }

        return results

    def run(self, ports):
        results = {}
        if 137 in ports:
            results['services Name'] = self.service_name_scan()

        if 139 in ports or 445 in ports:
            results['smb info '] = self.smb_scan()
            results['rpc_info'] = self.rpc_enumeration()

        return results