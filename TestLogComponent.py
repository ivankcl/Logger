import unittest
import time 

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
            contents = file.readlines()
            self.assertEqual(test_message, contents[-2])
            self.assertEqual(test_message_2, contents[-1])


if __name__ == '__main__':
    unittest.main()

        