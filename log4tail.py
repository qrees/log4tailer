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


import os,sys,re,getpass,logging
import logging.config
from optparse import OptionParser
from log4tailer import LogTailer,LogColors,Log,Properties
from log4tailer import notifications
from log4tailer.Configuration import MailConfiguration

import resource	


logging.basicConfig(level = logging.WARNING)
logger = logging.getLogger('log4tail')

def parseConfig(configfile):
    properties = Properties.Property(configfile)
    properties.parseProperties()
    return properties

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
    parser = OptionParser()
    parser.add_option("-c","--config",dest="configfile",
                    help="config file with colors")
    parser.add_option("-p","--pause",dest="pause",help="pause between tails")
    parser.add_option("--throttle",dest="throttle",
                    help="throttle output, slowsdown")
    parser.add_option("-i","--inact",dest="inactivity",
                    help="monitors inactivity in log given inactivity seconds")
    parser.add_option("-s","--silence",action="store_true",dest="silence",
                    help="tails in silence, no printing")
    parser.add_option("-n",dest="tailnlines",
                    help="prints last N lines from log")
    parser.add_option("-t","--target",dest="target",
                    help="emphasizes a line in the log")
    parser.add_option("-m","--mail",action="store_true",dest="mail",
                    help="notification by mail when a fatal is found")
    parser.add_option("-r","--remote",action="store_true",dest="remote",
                    help="remote tailing over ssh")
    parser.add_option("-f","--filter",dest="filter",
                    help="filters log traces, tail and grep")
    (options,args) = parser.parse_args()
    # defaults 
    pause = 1
    silence = False 
    throttle = 0
    printAction = notifications.Print()
    actions = [printAction]
    nlines = False
    target = None
    fromAddress = None
    toAddress = None
    properties = None
    logcolors = LogColors.LogColors()
    alt_config = os.path.expanduser('~/.log4tailer')
    config = options.configfile or alt_config
    if os.path.exists(config):
        logger.info("Configuration file [%s] found" % config)
        properties = parseConfig(config)
        logcolors.parseConfig(properties)
    if options.pause:
        pause = int(options.pause)
    if options.throttle:
        throttle = float(options.throttle)
    if options.silence:
        mailAction = notifications.Mail(MailConfiguration.configMail())
        actions.append(mailAction)
        mailAction.connectSMTP()
        silence = True
    if options.mail:
        mailAction = MailConfiguration.setupMailAction()
        actions.append(mailAction)
    if options.filter:
        # overrides Print notifier
        actions[0] = notifications.Filter(re.compile(options.filter))
    if options.tailnlines:
        nlines = int(options.tailnlines)
    if options.target:
        target = options.target
    if options.inactivity:
        inactivityAction = notifications.Inactivity(options.inactivity, properties)
        if inactivityAction.getNotificationType() == 'mail':
            if options.mail or options.silence:
                inactivityAction.setMailNotification(actions[len(actions)-1])
            else:
                mailAction = MailConfiguration.setupMailAction()
                inactivityAction.setMailNotification(mailAction)
        actions.append(inactivityAction)
    
    if options.remote:
        from log4tailer import SSHLogTailer
        tailer = SSHLogTailer.SSHLogTailer(logcolors,target,pause,
                                           throttle,silence,
                                           printAction,
                                           properties)
        if not tailer.sanityCheck():
            print "missing config file parameters"
            sys.exit()
        tailer.createCommands()
        try:
            tailer.createChannels()
        except Exception,e:
            print "Could not connect"
            print "Trace [%s]" % e
            sys.exit()
        tailer.tailer()
        sys.exit()
    tailer = LogTailer.LogTailer(logcolors,target,pause,
                                 throttle,silence,
                                 actions,
                                 properties)
    if args[0] == '-':
        tailer.pipeOut()
        sys.exit()
    for i in args:
        log = Log.Log(i,properties,options)
        tailer.addLog(log)
    if nlines:
        try:
            tailer.printLastNLines(nlines)
            print "Ended log4tailer, because colors are fun"
            sys.exit()
        except KeyboardInterrupt:
            print "Ended log4tailer, because colors are fun"
            sys.exit()
    tailer.tailer()
    sys.exit()

if __name__ == '__main__':
    main()
