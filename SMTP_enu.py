import socket

class SMTP_Enumeration:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.timeout = self.socket.settimeout(5)

    def connect(self, ip, port):
        self.socket.connect((ip, port))
        return self.socket.recv(1024).decode()

    def send_command(self, command):
        self.socket.sendall(f'{command}'.encode())
        print(f"[*] sending {command.strip()} ...")
        return self.socket.recv(1024).decode()

    def disconnect(self):
        self.socket.close()

    def enumerate(self, ip, port):
        results = {}
        try:
            results['banner'] = self.connect(ip, port)
            results['EHLO'] = self.send_command('EHLO attaker\r\n')
            results['verify'] = self.send_command('VRFY root\r\n')
            results['help'] = self.send_command('HELP\r\n')
            results['expn'] = self.send_command('EXPN staff\r\n')
            results['noop'] = self.send_command('NOOP\r\n')
            results['quit'] = self.send_command('QUIT\r\n')
        finally:
            self.disconnect()

        return results