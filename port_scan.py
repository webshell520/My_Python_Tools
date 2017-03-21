#-*-coding=utf-8-*-
import socket
import time
import Queue
import threading
from colorama import init,Fore
init(autoreset=True)
import sys

class PortScanner(object):

    def __init__(self,url):
        domain=url.replace('https://','').replace('http://','').replace('/','')
        try:
            self.IP = socket.gethostbyname(domain)
        except socket.gaierror:
            print Fore.RED+'[!]Connect Error '+domain
        self.port_range = (1,65536)
        self.print_lock = threading.Lock()#锁
        self.timeout = 2
        self.count=0
        self.openlist = []#结果列表
        self.verbose = True#是否输出详细内容

    #建立socket请求
    def _portscan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        # Tries to establish a connection to port, and append to list of open ports
        try:
            con = s.connect((self.IP, port))

            self.print_lock.acquire()
            print Fore.LIGHTWHITE_EX+ '\t'+str(port)+'\t0pen'
            self.print_lock.release()
            response = s.recv(1024)
            if self.verbose:
                self.openlist.append({port:response})

            s.close()
        # If the connection fails, tries to establish HTTP connection if port is a common HTTP port
        except socket.timeout:
            pass
        except socket.error:
            pass

    def _threader(self):
        while True:
            self.worker = self.q.get()
            self.count += 1
            print str(abs(round(0-(float(self.count)/float(65535)*100),2)))+'\r',
            self._portscan(self.worker)
            self.q.task_done()

    def scan(self):
        '''Scans ports of an IP address. Use getIP() to find IP address of host.
        '''

        # Creates queue to hold each thread
        self.q = Queue.Queue()
        for x in range(30):
            t = threading.Thread(target=self._threader)
            t.daemon = True
            t.start()
        # Adds workers to queue
        for worker in range(self.port_range[0], self.port_range[1]):
            self.q.put(worker)


        self.q.join()

    def run(self):
        self.scan()
        for i in self.openlist:
            for k,v in i.items():
                print str(k)+' info=>',v
if __name__=='__main__':
    if len(sys.argv)>=2:
        run=PortScanner(sys.argv[1])
        run.run()
    else:
        print 'scanner.py 127.0.0.1'


