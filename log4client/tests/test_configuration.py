import unittest
from log4tailer.configuration import DefaultConfig


class TestConfiguration(unittest.TestCase):

    def test_instantiates_defaultconfig(self):
        default_config = DefaultConfig()
        self.assertTrue(isinstance(default_config, DefaultConfig))

    def test_gets_property(self):
        default_config = DefaultConfig()
        throttle = default_config.throttle
        assert throttle == 0
