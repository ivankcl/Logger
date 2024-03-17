from datetime import datetime

import threading
import os
import time

class LogComponent():

    log_folder_path = 'Log'

    def __init__(self):
        self.message_queue = []
        self.running = True
        if not os.path.exists(self.log_folder_path):
            os.makedirs(self.log_folder_path)

        self.background_thread = threading.Thread(target=self._background_writing)
        self.background_thread.start()

    def write(self, message: str):
        self.message_queue.append(message)

    def stop(self, wait_for_outstanding_log = True):
        self.running = False
        self.background_thread.join()


    def _background_writing(self):
        while (self.running):
            if (self.message_queue):
                message = self.message_queue.pop(0)
                self._write_to_file(message)
            else:
                time.sleep(0.1)

    def _write_to_file(self, message: str):
        log_name = f'log_{datetime.now().strftime("%Y%m%d")}.txt'
        log_path = os.path.join(self.log_folder_path, log_name)
        with open(log_path, "a") as file:
            file.write(message + '\n')
        
if __name__ == '__main__':
    logComponent = LogComponent()
    for _ in range(10):
        logComponent.write('Hello World')
    
    time.sleep(5)
    logComponent.stop()