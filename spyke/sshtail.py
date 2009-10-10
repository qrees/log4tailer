#!/usr/bin/env python

import paramiko,time
import getpass,sys,select
sys.path.append('..')

from log4tailer.Message import Message
from log4tailer.LogColors import LogColors
from log4tailer.Actions import PrintAction

sshclient = paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
if len(sys.argv) != 3:
    print "need to provide username and password"
    sys.exit()
yourhostname = sys.argv[1]
yourusername = sys.argv[2]
print "hostname: "+yourhostname
print "username: "+yourusername
sshclient.connect(yourhostname,username=yourusername,password=getpass.getpass())
transport = sshclient.get_transport()
sshChannel = transport.open_session()


message = Message(LogColors())
action = PrintAction.PrintAction()

sshChannel.exec_command('tail -F out.log')
while True:
    try:
        rr,wr,xr = select.select([sshChannel],[],[],0.0)
        #print "after select"
        if len(rr)>0:
            lines = sshChannel.recv(1024).split('\n')
            for line in lines:
                print "line :" + line
                message.parse(line,(None,None,None))
                action.triggerAction(message,'anylog')
            
            #print sshChannel.recv(1024).rstrip()
        else:
            time.sleep(1)

    except:
        print "\nfinishing ..."
        sshChannel.close()
        stdin,stdout,stderr = sshclient.exec_command('pgrep -f -x \"tail -F out.log\"')
        procid = stdout.readlines()[0].rstrip()
        print procid
        # is process still alive after closing channel?
        if procid:
            # kill it
            killprocid = 'kill -9 '+procid
            stdin,stdout,stderr = sshclient.exec_command(killprocid)
        #sshChannel.shutdown(2)
        sshclient.close()
        sys.exit()
