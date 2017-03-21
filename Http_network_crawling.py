#!/usr/bin/env python
#-*-coding=utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import sys
import Queue
import threading
import argparse
import requests
from IPy import IP

printLock = threading.Semaphore(1)  #lock Screen print
TimeOut = 5  #request timeout

#User-Agent
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36','Connection':'close'}

class crawl(object):
    def __init__(self,ip,filename,port,threadnum,writename='_result.txt'):
        self.queue=Queue.Queue()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': '*/*',
            'Referer': 'http://www.google.com',
            'Cookie': 'whoami=21232f297a57a5a743894a0e4a801fc3'
        }
        self.ips=ip
        self.ports=port
        self.threadnum=threadnum
        self.writename=writename
        self.filename=filename
        self.print_lock=threading.Lock()

    def _request(self,url):
        try:
            return requests.get(url, timeout=10,headers=self.headers)
        except requests.exceptions.ConnectTimeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.Timeout:
            return False

    def load_queue(self):
        if self.ips !='':
            self.ips= list(IP(self.ips))
            for ip in self.ips:
                for port in self.ports:
                    self.queue.put('http://'+str(ip)+':'+str(port))
        if self.filename !='':
            with open(self.filename) as file:
                domains=file.readlines()
                for domain in domains:
                    for port in self.ports:
                        domain=domain.strip()
                        if 'http' not in domain:
                            self.queue.put('http://'+domain+':'+str(port))
                        else:
                            self.queue.put(domain+ ':' + str(port))

    def _write_file(self,content):
        with open(self.writename,'a+') as file:
            file.write(content+'\n')

    def _message(self,header,_text):
        if header:
            try:
                Server = header['Server']
            except Exception:
                Server = 'Unknow'

            try:
                Powered = header['X-Powered-By']
            except:
                Powered = 'Unknow'
            print Server, Powered

        if _text:
            title=re.search('<title>(.*?)</title>',_text)
            if title:
                print title.group(1)[:30]


    def scan(self):
        while True:
            if self.queue.empty():
                break
            target=self.queue.get()
            start=True

            with self.print_lock:
                #print target
                pass
            html=self._request(target)

            try:#如果返回bool就不进行扫描了
                html.status_code
            except TypeError:
                start=False
            except AttributeError:
                start=False
            with self.print_lock:
                if start:
                    try:
                        banner=html.headers['server']
                    except KeyError:
                        banner='Unknow'

                    try:
                        Powered=html.headers['X-Powered-By']
                    except KeyError:
                        Powered='Unknow'

                    title=re.search(r'<title>(.*)</title>',html.text)
                    if title:
                        title= title.group(1)
                    else:
                        title='None'

                    _write=u'【'+target+u'】\t【'+Powered+u'】\t【'+banner+u'】\t【'+title+u'】'
                    self._write_file(_write)
                    message= "|%-26s|%-8s|%-10s|%-20s|" % (target[:26], Powered[:8], banner[:10], title[:20])
                    print message
                    print '+'+'+'.rjust(27,'-')+'+'.rjust(10,'-')+'+'.rjust(11,'-')+'+'.rjust(21,'-')
    def run(self):
        self.load_queue()
        print '+'+'URL'.center(26,'-')+'+'+'Powered'.center(10,'-')+'+'+'BANNER'.center(11,'-')+'+'+'TITLE'.center(20,'-')+'+'
        threads=[]
        for i in range(int(self.threadnum)):
            t=threading.Thread(target=self.scan)
            threads.append(t)
            t.start()

        for i in threads:
            i.join()

parse = argparse.ArgumentParser()
parse.add_argument("--ip", dest="ip",default='',metavar='\t --ip 123.45.25.0/24')
parse.add_argument("--file", dest="filename", default='',metavar='\t--file scan.txt')
parse.add_argument("--ports", dest="ports", default='80',metavar='\t--ports 80,8080(default 80)')
parse.add_argument("--threadnum", dest="threadnum", default=30, type=int,metavar='\t --threadnum 30 (default 30)')
parse.add_argument("--save", dest="save",default='scan_result.txt',metavar='\t --save res.txt')
args = parse.parse_args()

def main(args):
    ip=args.ip
    file=args.filename
    port=args.ports.split(',')
    threadnum=args.threadnum
    save=args.save
    r = crawl(ip=ip, filename=file, port=port,threadnum=threadnum,writename=save)
    r.run()
if __name__ == "__main__":
    if len(sys.argv)>1:
        main(args)
    else:
        parse.print_help()

