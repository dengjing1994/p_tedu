from socket import *
from threading import Thread


class TankHost():
    def __init__(self):
        self.get_sfd()
        self.get_rfd()
    
    def get_sfd(self):
        self.sfd = socket()
        self.sfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sfd.bind(('127.0.0.1', 9527))
    
    def get_rfd(self):
        self.rfd = socket()
        self.rfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.rfd.bind(('127.0.0.1', 9528))
    
    def start_host(self):
        t = Thread(target=self.pjoin)
        t.daemon = True
        t.start()
        self.sfd.listen(5)
        while 1:
            try:
                cfd, addr = self.sfd.accept()
            except KeyboardInterrupt:
                self.sfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                print('ERROR:', e)
                continue
            msg = cfd.recv(4096).decode()
            if msg == 'tank_c':
                self.p2 = Thread(target=self.handler, args=(cfd,))
                self.p2.start()
                break
            else:
                continue
        self.main()
    
    def pjoin(self):
        self.p2.join()
    
    def handler(self, cfd):
        cfd.send(r'tank')
        while 1:
            msg = sfd.recv(4096).decode()
            self.solve_msg(msg)
            msg = self.get_msg()
            sfd.send(msg.encode())