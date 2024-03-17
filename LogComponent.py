from datetime import datetime

import threading
import os
import time
import queue

class LogComponent():

    log_folder_path = 'Log'

    def __init__(self):
        self.message_queue = queue.Queue()
        self.running = True
        if not os.path.exists(self.log_folder_path):
            os.makedirs(self.log_folder_path)

        self.background_thread = threading.Thread(target=self._background_writing)
        self.background_thread.start()

    def write(self, message: str):
        self.message_queue.put(message)

    def stop(self, wait_for_outstanding_log: bool = True):
        if (wait_for_outstanding_log):
            while (not self.message_queue.empty()):
                time.sleep(0.1)

        self.running = False
        self.background_thread.join()

    def _background_writing(self):
        while (self.running):
            if (not self.message_queue.empty()):
                try: 
                    message = self.message_queue.get(timeout=0.1)
                    self._write_to_file(message)
                except queue.Empty:
                    pass # Do nothing if the queue is empty

    def _write_to_file(self, message: str):
        log_name = f'log_{datetime.now().strftime("%Y%m%d")}.txt'
        log_path = os.path.join(self.log_folder_path, log_name)
        with open(log_path, "a") as file:
            file.write(message + '\n')
        
if __name__ == '__main__':
    logComponent = LogComponent()
    for _ in range(10):
        logComponent.write('Hello World')
    logComponent.stop()