import os
import sys
import re
import logging
from . import logtailer, logfile, propertyparser
from . import notifications
from .utils import setup_mail
import time

__version__ = "3.0.8"
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('log4tail')


def parse_config(configfile):
    properties = propertyparser.Property(configfile)
    properties.parse_properties()
    return properties

def set_mail_connect(properties):
    mailAction = setup_mail(properties)
    mailAction.connectSMTP()
    return mailAction

def setup_config(options, default_config):
    colors = default_config.logcolors
    actions = default_config.actions
    config_file = options.configfile or default_config.alt_config
    if options.version:
        print __version__
        sys.exit(0)
    if os.path.exists(config_file):
        logger.info("Configuration file [%s] found" % config_file)
        default_config.properties = parse_config(config_file)
        colors.parse_config(default_config.properties)
    properties = default_config.properties
    actions.append(notifications.Print(properties))
    if options.pause:
        default_config.pause = int(options.pause)
    if options.throttle:
        throttle = float(options.throttle)
        default_config.throttle = throttle
    if options.silence and properties:
        mail_action = set_mail_connect(properties)
        actions.append(mail_action)
        default_config.silence = True
    if options.nomailsilence:
        # silence option with no mail
        # up to user to provide notification by mail
        # or do some kind of reporting
        default_config.silence = True
    if options.mail and properties:
        mail_action = set_mail_connect(properties)
        actions.append(mail_action)
    if options.filter:
        # overrides Print notifier
        actions[0] = notifications.Filter(re.compile(options.filter))
    if options.ignore:
        # overrides Print notifier
        actions[0] = notifications.IgnoreAction(re.compile(options.ignore))
    if options.tailnlines:
        default_config.nlines = int(options.tailnlines)
    if options.target:
        default_config.target = options.target
    if options.inactivity:
        inactivityAction = notifications.Inactivity(options.inactivity,
                properties)
        if inactivityAction.getNotificationType() == 'mail':
            if options.mail or options.silence:
                inactivityAction.setMailNotification(actions[len(actions) - 1])
            else:
                mail_action = set_mail_connect(properties)
                inactivityAction.setMailNotification(mail_action)
        actions.append(inactivityAction)
    if options.cornermark:
        cornermark = notifications.CornerMark(options.cornermark)
        actions.append(cornermark)
    if options.post and properties:
        default_config.post = True
        poster = notifications.Poster(properties)
        actions.append(poster)
    if options.executable and properties:
        executor = notifications.Executor(properties)
        actions.append(executor)
    if options.screenshot and properties:
        printandshoot = notifications.PrintShot(properties)
        actions[0] = printandshoot
    if options.slowdown:
        actions.append(notifications.SlowDown(default_config.tail_context))


def monitor(options, args, default_config, wait_for=time.sleep):
    if options.remote:
        from . import sshlogtailer
        tailer = sshlogtailer.SSHLogTailer(default_config)
        if not tailer.sanityCheck():
            print "missing config file parameters"
            sys.exit()
        tailer.createCommands()
        try:
            tailer.createChannels()
        except Exception, e:
            print "Could not connect"
            print "Trace [%s]" % e
            sys.exit()
        tailer.tailer()
        sys.exit()
    tailer = logtailer.LogTailer(default_config, wait_for)

    if args[0] == '-':
        tailer.pipeOut()
        sys.exit()
    for i in args:
        log = logfile.Log(i, default_config.properties, options)
        tailer.addLog(log)
    if default_config.nlines:
        try:
            tailer.printLastNLines(default_config.nlines)
            print "Ended log4tailer, because colors are fun"
            sys.exit()
        except KeyboardInterrupt:
            print "Ended log4tailer, because colors are fun"
            sys.exit()
    tailer.tailer()


def main(options, args, default_config):
    setup_config(options, default_config)
    monitor(options, args, default_config)
