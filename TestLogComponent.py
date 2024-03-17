import unittest
from datetime import datetime
from freezegun import freeze_time
import time 
import os

from LogComponent import LogComponent

class TestLogComponent(unittest.TestCase):

    def setUp(self):
        self.logger = LogComponent()

    def tearDown(self):
        self.logger.stop()

    def test_write(self):
        test_message = 'Test: !\"#$%&\'()*+,-./0123456789:;<=>?@\n'
        test_message_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        log_path = self.logger._get_file_path()

        self.logger.write('\n')
        self.logger.write(test_message)
        self.logger.write(test_message_2)

        # Allow time for the logger to write
        time.sleep(0.5)

        with open(log_path, 'r') as file:
            messages = file.readlines()
            self.assertEqual(test_message, messages[-2])
            self.assertEqual(test_message_2, messages[-1])

    @freeze_time(datetime(2024, 3, 17, 23, 59, 58))
    def test_write_before_midnight(self):
        # time_before = datetime(2024, 3, 17, 23, 59, 58)
        from LogComponent import LogComponent
        logger = LogComponent()

        test_message_before = 'Test message before midnight'
        log_path_before = logger._get_file_path()
        logger.write('\n')
        logger.write(test_message_before)

        time.sleep(0.5)

        with open(log_path_before, "r") as file:
            messages = file.readlines()
            self.assertEqual(test_message_before, messages[-1])

        self.assertEqual(os.path.join(logger.log_folder_path, 'log_20240317.txt'), log_path_before)

        logger.stop()

    @freeze_time(datetime(2024, 3, 18, 0, 0, 0))
    def test_write_after_midnight(self):

        from LogComponent import LogComponent
        logger = LogComponent()

        test_message_after = 'Test message after midnight'
        log_path_after = logger._get_file_path()
        logger.write('\n')
        logger.write(test_message_after)

        time.sleep(0.5)

        with open(log_path_after, "r") as file:
            messages = file.readlines()
            self.assertEqual(test_message_after, messages[-1])

        self.assertEqual(os.path.join(logger.log_folder_path, 'log_20240318.txt'), log_path_after)

        logger.stop()

    def test_stop_with_wait(self):
        test_message = 'Test: !\"#$%&\'()*+,-./0123456789:;<=>?@\n'
        test_message_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        log_path = self.logger._get_file_path()

        for _ in range(10):
            self.logger.write('\n')
            self.logger.write(test_message)
            self.logger.write(test_message_2)

        remaining_message = self.logger.stop(wait_for_outstanding_log=True)

        self.assertFalse(self.logger.background_thread.is_alive())
        self.assertEqual(len(remaining_message), 0)
        with open(log_path, 'r') as file:
            messages = file.readlines()
            self.assertEqual(test_message, messages[-2])
            self.assertEqual(test_message_2, messages[-1])

    def test_stop_without_wait(self):
        test_message = 'Test: !\"#$%&\'()*+,-./0123456789:;<=>?@\n'
        test_message_2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

        self.logger.write('\n')
        self.logger.write(test_message)
        self.logger.write(test_message_2)

        self.logger.stop(wait_for_outstanding_log=False)
        self.assertFalse(self.logger.background_thread.is_alive())

if __name__ == '__main__':
    unittest.main()