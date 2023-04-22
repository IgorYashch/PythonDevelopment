import cmd
import threading
import readline
import socket
import time

class NetcatCmd(cmd.Cmd):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.prompt = "netcat> "
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        self.print_thread = threading.Thread(target=self.print_from_server)
        self.print_thread.start()
        self.last_message = None

    def print_from_server(self):
        while True:
            msg = self.sock.recv(1024).decode()
            code, msg = msg[0], msg[1:]
            if code == '0':
                print(f"\n{msg}{self.prompt}{readline.get_line_buffer()}", end="", flush=True)
                self.last_message = None
            elif code == '1':
                self.last_message = msg
            

    def do_who(self, _):
        self.sock.sendall(b"who\n")

    def do_cows(self, _):
        self.sock.sendall(b"cows\n")

    def do_login(self, cow_name):
        self.sock.sendall(f"login {cow_name}\n".encode())

    def do_say(self, line):
        self.sock.sendall(f"say {line}\n".encode())

    def do_yield(self, message):
        self.sock.sendall(f"yield {message}\n".encode())

    def do_quit(self, _):
        self.sock.sendall(b"quit\n")
        self.sock.close()
        return True

    def complete_login(self, text, line, begidx, endidx):
        self.sock.sendall(b"cows complete\n")
        while self.last_message is None:
            time.sleep(0.1)
        cows = self.last_message.split()    
        return [cow for cow in cows if cow.startswith(text)]

    def complete_say(self, text, line, begidx, endidx):
        self.sock.sendall(b"who complete\n")
        while self.last_message is None:
            time.sleep(0.1)
        users = self.last_message.split()
        return [user for user in users if user.startswith(text)]

if __name__ == '__main__':
    server_ip = '0.0.0.0'
    server_port = 1337
    netcat = NetcatCmd(server_ip, server_port)
    netcat.cmdloop()
