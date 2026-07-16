import socket
import threading

class port_scan:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()
        
    def scan_port(self, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f"[+] Port {port} is open")
            
            sock.close()


    def scan(self, start_port=1, end_port=65535):
        print(f"\n[#] Scanning Target: {self.target} from port {start_port} to {end_port}")
        
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        return self.open_ports 