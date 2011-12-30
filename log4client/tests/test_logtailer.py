import unittest
import sys
import mocker
import os
import re
from mocker import ANY
from log4tailer import reporting
from log4tailer.logtailer import LogTailer
from log4tailer.configuration import DefaultConfig
from log4tailer import notifications
from log4tailer.logfile import Log
from log4tailer.propertyparser import Property
from log4tailer.logtailer import hasRotated
import log4tailer
from .utils import MemoryWriter

SYSOUT = sys.stdout


def getDefaults():
    default_config = DefaultConfig()
    default_config.alt_config = None
    return default_config


class TestResume(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()

    def testshouldReturnTrueifMailAlreadyinMailAction(self):
        mailaction_mock = self.mocker.mock(notifications.Mail)
        self.mocker.replay()
        defaults = getDefaults()
        defaults.actions = [mailaction_mock]
        logtailer = LogTailer(defaults)
        self.assertEqual(True, logtailer.mailIsSetup())

    def _setupAConfig(self, method='mail'):
        fh = open('aconfig', 'w')
        fh.write('inactivitynotification = ' + method + '\n')
        fh.close()

    def testshouldReturnFalseMailNotSetup(self):
        self._setupAConfig()
        properties = Property('aconfig')
        properties.parse_properties()
        defaults = getDefaults()
        defaults.properties = properties
        logtailer = LogTailer(defaults)
        self.assertEqual(False, logtailer.mailIsSetup())

    def testReturnsFalseMailOrInactivityActionNotificationNotEnabled(self):
        logtailer = LogTailer(getDefaults())
        self.assertEqual(False, logtailer.mailIsSetup())

    def testPipeOutShouldSendMessageParseThreeParams(self):
        sys.stdin = ['error > one error', 'warning > one warning']
        sys.stdout = MemoryWriter()
        defaults = getDefaults()
        defaults.actions.append(notifications.Print())
        logtailer = LogTailer(defaults)
        logtailer.pipeOut()
        self.assertTrue('error > one error' in sys.stdout.captured[0])

    def testResumeBuilderWithAnalyticsFile(self):
        sys.stdout = MemoryWriter()
        reportfile = 'reportfile.txt'
        configfile = 'aconfig'
        fh = open(configfile, 'w')
        fh.write('analyticsnotification = ' + reportfile + '\n')
        fh.close()
        properties = Property(configfile)
        properties.parse_properties()
        defaults = getDefaults()
        defaults.properties = properties
        logtailer = LogTailer(defaults)
        resumeObj = logtailer.resumeBuilder()
        self.assertTrue(isinstance(resumeObj, reporting.Resume))
        self.assertEquals('file', resumeObj.getNotificationType())
        self.assertEquals(reportfile, resumeObj.report_file)

    def testResumeBuilderWithInactivityAction(self):
        defaults = getDefaults()
        defaults.actions = [notifications.Inactivity(5)]
        tailer = LogTailer(defaults)
        resume = tailer.resumeBuilder()
        self.assertTrue(isinstance(resume.notifiers[0],
            notifications.Inactivity))

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        sys.stdout = SYSOUT


class TestTailer(unittest.TestCase):
    log_name = 'out.log'

    def setUp(self):
        self.onelog = Log(self.log_name)
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'
        fh = open(self.log_name, 'w')
        fh.write(onelogtrace + '\n')
        fh.write(anotherlogtrace + '\n')
        fh.close()
        self.raise_count = 0

    def test_tailerPrintAction(self):
        onelogtrace = 'this is an info log trace'
        anotherlogtrace = 'this is a debug log trace'

        def write_log():
            fh = open(self.log_name, 'a')
            fh.write(onelogtrace + '\n')
            fh.write(anotherlogtrace + '\n')
            fh.close()
            self.raise_count += 1

        def wait_for(secs):
            if self.raise_count == 0:
                write_log()
                return
            raise KeyboardInterrupt

        sys.stdout = MemoryWriter()
        tailer = LogTailer(getDefaults(), wait_for)
        tailer.addLog(self.onelog)
        tailer.tailer()
        finish_trace = re.compile(r'because colors are fun')
        found = False
        for _, line in enumerate(sys.stdout.captured):
            if finish_trace.search(line):
                found = True
        if not found:
            self.fail()

    def tearDown(self):
        sys.stdout = SYSOUT
        if os.path.exists(self.log_name):
            os.remove(self.log_name)


class TestInit(unittest.TestCase):
    def setUp(self):
        self.mocker = mocker.Mocker()

    def _options_mocker_generator(self, mock, params):
        for key, val in params.iteritems():
            getattr(mock, key)
            self.mocker.result(val)

    class OptionsMock(object):
        def __init__(self):
            pass

        def __getattr__(self, name):
            if name == 'inactivity':
                return True
            elif name == 'configfile':
                return "anythingyouwant"
            return False

    def test_monitor_inactivity_nomail(self):
        options_mock = self.mocker.mock()
        options_mock.inactivity
        self.mocker.result(True)
        self.mocker.count(1, 2)
        params = {'configfile': 'anythingyouwant',
                'version': False,
                'filter': False,
                'ignore': False,
                'tailnlines': False,
                'target': False,
                'cornermark': False,
                'executable': False,
                'post': False,
                'pause': False,
                'throttle': False,
                'silence': False,
                'mail': False,
                'nomailsilence': False,
                'screenshot': False}
        self._options_mocker_generator(options_mock, params)
        default_config = DefaultConfig()
        self.mocker.replay()
        log4tailer.setup_config(options_mock, default_config)
        actions = default_config.actions
        self.assertEquals(2, len(actions))
        self.assertTrue(isinstance(actions[0], notifications.Print))
        self.assertTrue(isinstance(actions[1], notifications.Inactivity))
        self.assertFalse(isinstance(actions[0], notifications.CornerMark))

    def test_monitor_inactivity_withmail(self):
        properties_mock = self.mocker.mock()
        properties_mock.get_value('inactivitynotification')
        self.mocker.result('mail')
        properties_mock.get_value('print_hostname')
        self.mocker.result('false')
        properties_mock.get_keys()
        self.mocker.result([])
        default_config = getDefaults()
        default_config.properties = properties_mock
        utils_mock = self.mocker.replace('log4tailer.utils.setup_mail')
        class MailActionMock(object):
            def __init__(self):
                pass
            def connectSMTP(self):
                pass
        utils_mock(ANY)
        self.mocker.result(MailActionMock())
        self.mocker.replay()
        log4tailer.setup_config(self.OptionsMock(), default_config)
        actions = default_config.actions
        self.assertEquals(2, len(actions))
        self.assertTrue(isinstance(actions[0], notifications.Print))
        self.assertTrue(isinstance(actions[1], notifications.Inactivity))
        self.assertFalse(isinstance(actions[0], notifications.CornerMark))

    def test_corner_mark_setup(self):
        options_mock = self.mocker.mock()
        options_mock.cornermark
        self.mocker.count(1, 2)
        self.mocker.result(True)
        params = {'configfile': 'anythingyouwant',
                'version': False,
                'filter': False,
                'ignore': False,
                'tailnlines': False,
                'target': False,
                'executable': False,
                'pause': False,
                'throttle': False,
                'silence': False,
                'mail': False,
                'inactivity': False,
                'nomailsilence': False,
                'post': False,
                'screenshot': False}
        self._options_mocker_generator(options_mock, params)
        default_config = DefaultConfig()
        self.mocker.replay()
        log4tailer.setup_config(options_mock, default_config)
        actions = default_config.actions
        self.assertEquals(2, len(actions))
        self.assertTrue(isinstance(actions[0], notifications.Print))
        self.assertTrue(isinstance(actions[1], notifications.CornerMark))

    def test_daemonized_resumedaemonizedtrue(self):
        default_config = getDefaults()
        default_config.silence = True
        logtailer = LogTailer(default_config)
        resumeObj = logtailer.resumeBuilder()
        self.assertTrue(isinstance(resumeObj, reporting.Resume))
        self.assertEquals('print', resumeObj.getNotificationType())
        self.assertTrue(resumeObj.is_daemonized)

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()


class LogRotated(Log):
    """A log that has rotated based upon a difference on the inode/size in
    between tails. Normally, this is due to a truncated log or current size is
    less than the actual size of the log.
    """

    def __init__(self, with_same_inode=False, with_same_size=False,
            with_gt_size=False):
        self.inode = 1001
        self.size = 2000
        self.path = '/alog.log'
        self.with_same_inode = with_same_inode
        self.with_same_size = with_same_size
        self.with_gt_size = with_gt_size

    def getcurrInode(self):
        if not self.with_same_inode:
            return self.inode + 1
        return self.inode

    def closeLog(self):
        pass

    def openLog(self):
        pass

    def seekLogEnd(self):
        pass

    def getcurrSize(self):
        if self.with_same_size:
            return self.size
        elif self.with_gt_size:
            return self.size + 100
        return self.size - 1


class TestHasRotatedCase(unittest.TestCase):

    def test_rotates_inode_different(self):
        log = LogRotated()
        self.assertTrue(hasRotated(log))

    def test_rotates_size_differs(self):
        log = LogRotated(with_same_inode=True)
        self.assertTrue(hasRotated(log))

    def test_norotation_sameinode_currsize_gt(self):
        log = LogRotated(with_same_inode=True, with_gt_size=True)
        self.assertFalse(hasRotated(log))

    def test_norotation_sameinode_currsize_eq(self):
        log = LogRotated(with_same_inode=True, with_same_size=True)
        self.assertFalse(hasRotated(log))
