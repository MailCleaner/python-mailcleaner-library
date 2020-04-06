import unittest.mock as mock
import os
from mailcleaner.logger import *


def test_log_file_existing_folder():
    with mock.patch('builtins.open') as mopen:
        __mcLogger = McLogger(name="test_log_file_existing_folder")
        __mcLogger.info("test")
        mopen.stop()
        assert(mopen.called and mock.call(1).write('\n') in mopen.mock_calls)

def test_log_file_create_folder():
    with mock.patch('os.mkdir') as mdir, \
         mock.patch('builtins.open') as mopen:
        __mcLogger = McLogger(name="test_log_file_create_folder", project="test")
        mopen.stop
        assert(mopen.called and mdir.called)

def test_log_level_environ():
    with mock.patch('builtins.open') as mopen:
        os.environ["LOG_LEVEL"] = MCLogLevel.debug.value
        __mcLogger = McLogger(name="test_log_level_environ")
        __mcLogger.warn("test")
        assert(mopen.called and mock.call(1).write('\n') in mopen.mock_calls)