#!/usr/bin/env python 

# Log4Tailer: A multicolored python tailer for log4J logs
# Copyright (C) 2008 Jordi Carrillo Bosch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


## TODO monitor inactivity in logs
## post in web using Django Action
## Grab smtp properties from file


import os,sys,re,getpass
from optparse import OptionParser
from log4tailer import LogTailer,LogColors,Log
from log4tailer.Actions import PrintAction,MailAction
import resource	

def startupNotice():
    notice = """Log4Tailer  Copyright (C) 2008 Jordi Bosch
        This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
            This is free software, and you are welcome to redistribute it
                under certain conditions; type `show c' for details."""
    print notice           

def main():
    if len(sys.argv[1:]) == 0:
        print "Provide at least one log"
        sys.exit()
    color = LogColors.LogColors()
    parser = OptionParser()
    parser.add_option("-c","--config",dest="configfile",help="config file with colors")
    parser.add_option("-p","--pause",dest="pause",help="pause between tails")
    parser.add_option("--throttle",dest="throttle",help="throttle output, slowsdown")
    parser.add_option("-i","--inact",dest="inactivity",help="monitors inactivity in log")
    parser.add_option("-s","--silence",action="store_true",dest="silence",help="tails in silence, no printing")
    parser.add_option("-n",dest="tailnlines",help="prints last N lines from log")
    parser.add_option("-t","--target",dest="target",help="emphasizes a line in the log")
    (options,args) = parser.parse_args()
    
    # defaults 
    pause = 1
    silence = False 
    throttle = 0
    # default action is printing STDOUT
    action = PrintAction.PrintAction()
    nlines = False
    target = None
    fromAddress = None
    toAddress = None


    if options.configfile:
        color.parseConfig(options.configfile)
    if options.pause:
        pause = int(options.pause)
    if options.throttle:
        throttle = int(options.throttle)
    if options.silence:
        # silence mode enables sendSmtp Action.
        # There could be other actions like Post to Web Page
        # by using Django.
        hostname = raw_input("Host name for your SMTP account?\n")
        username = raw_input("Your username?\n")
        pwd = getpass.getpass()
        fromAddress = raw_input("Alerts send From Address:\n")
        toAddress = raw_input("Alerts send To Address:\n")
        action = MailAction.MailAction(fromAddress,toAddress,hostname,username,pwd)
        action.connectSMTP()
        silence = True
    if options.tailnlines:
        nlines = int(options.tailnlines)
    if options.target:
        target = options.target

    
    tailer = LogTailer.LogTailer(color,pause,throttle,silence,action,fromAddress,toAddress)
    for i in args:
        log = Log.Log(i,color,target)
        tailer.addLog(log)
    #startupNotice()
    if nlines:
        tailer.printLastNLines(nlines)
        sys.exit()
    tailer.tailer()
    sys.exit()



if __name__ == '__main__':
    main()
