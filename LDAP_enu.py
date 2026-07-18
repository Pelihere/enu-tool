import subprocess


class LDAP_Enumeration:
    def __init__(self, target):
        self.target = target
        self.baseDn = None

    def anonmyous_enu(self, port):
        try:
            if port in [389, 636]:
                anonymousState = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base"],
                                                capture_output=True,
                                                text=True)
                print("ldapsearch is running for anonymouse state ...")
        except FileNotFoundError:
            print("ldapsearch is not installed!")
        except Exception as e:
            print(f"soemthing went wrong while executing ldapsearch. Error : \n {e}")

        return {
            "tool": "ldapsearch",
            "success": anonymousState.returncode == 0,
            "stdout": anonymousState.stdout,
            "stderr": anonymousState.stderr,
        }

    def RootDSE_enu(self):
        try:
            rootdseState = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-s", "base", "namingContexts"], 
                                            capture_output=True, 
                                            text=True)
            
            for line in rootdseState.stdout.splitlines():
                if line.startswith("namingContexts:"):
                    self.baseDn = line.split(":", 1)[1].strip()
                    break

            print("ldapsearch is runnig for RootDSE enumeration ...")    
        except FileNotFoundError:
            print("ldapsearch is not installed!")
        except Exception as e:
            print(f"soemthing went wrong while executing ldapsearch. Error : \n {e}")

        return {
            "tool" : "ldapsearch",
            "success" : rootdseState.returncode == 0,
            "stdout" : rootdseState.stdout,
            "stderr" : rootdseState.stderr,
        }
    
    def domain_enu(self):
        try:
            domainInfo = subprocess.run(["ldapsearch", "-x", "-H", f"ldap://{self.target}", "-b", f"{self.baseDn}"], 
                                        capture_output=True,
                                        text=True)
            print("running ldapsearch for domain enumeration ...")
        except FileNotFoundError:
            print("ldapsearch is not installed!")
        except Exception as e:
            print(f"soemthing went wrong while executing ldapsearch. Error : \n {e}")
        
        return {
            "tool" : "ldapsearch",
            "success" : domainInfo.returncode == 0,
            "stdout" : domainInfo.stdout,
            "stderr" : domainInfo.stderr,
        }
    
    def ldap_walker(self, filter):
        try:
            res = subprocess.run(["ldapsearch", "-x", "-b", f"{self.baseDn}", f"(objectClass={filter})", "-H", f"ldap://{self.target}"],
                                capture_output=True,
                                text=True)
            print(f"running ldapsearch for {filter} enumeration ...")
        except FileNotFoundError:
            print("ldapsearch is not installed!")
        except Exception as e:
            print(f"soemthing went wrong while executing ldapsearch. Error : \n {e}")

        return {
            "tool" : "ldapsearch",
            "success" : res.returncode == 0,
            "stdout" : res.stdout,
            "stderr" : res.stderr,
        }

    def users_enu(self):
        return self.ldap_walker("user")
    
    def groups_enu(self):
        return self.ldap_walker("group")
    
    def computer_enu(self):
        return self.ldap_walker("computer")

    def organizationalUnits_enu(self):
        return self.ldap_walker("organizationalUnit")
    
    def run(self):
        results = {}

        self.RootDSE_enu()
        if self.baseDn is None:
            return None

        results['domain'] = self.domain_enu()
        results['user'] = self.users_enu()
        results['groups'] = self.groups_enu()
        results['computer'] = self.computer_enu()
        results['organzationalUnits'] = self.organizationalUnits_enu()

        return results 