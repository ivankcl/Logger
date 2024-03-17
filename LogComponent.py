import threading
import os
import time
import queue

from datetime import datetime

class LogComponent():

    def __init__(self, log_folder_path: str = 'Log'):

        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)

        self.log_folder_path = log_folder_path
        self.message_queue = queue.Queue()

        try:
            # To write asynchronously without blocking the main application, a new thread is created
            self.stop_event = threading.Event()
            self.background_thread = threading.Thread(target=self._background_writing)
            self.background_thread.start()
        except Exception as e:
            print('The thread could not be created: ', e)

    def write(self, message: str):
        try:
            # put() here is virtually atomic
            self.message_queue.put(message)
        except Exception as e:
            print('The message could not be logged: ', e)

    def stop(self, wait_for_outstanding_log: bool = True):

        try:
        
            if (not self.stop_event.is_set()):
                if (wait_for_outstanding_log):

                    # Write until empty
                    while (not self.message_queue.empty()):
                        time.sleep(0.1)

                self.stop_event.set()
                self.background_thread.join()

            # Return the list of messages that is not written to the log
            return list(self.message_queue.queue)
        except Exception as e:
            print('The logger could not be stopped: ', e)

    def _background_writing(self):

        # Background thread's main loop, asynchronous writing
        while (not self.stop_event.is_set()):
            if (not self.message_queue.empty()):
                try: 
                    message = self.message_queue.get(timeout=0.1)
                    self._write_to_file(message)
                except queue.Empty:
                    pass # Do nothing if the queue is empty
    
    def _get_file_path(self):
        log_name = f'log_{datetime.now().strftime("%Y%m%d")}.txt'
        log_path = os.path.join(self.log_folder_path, log_name)
        return log_path

    def _write_to_file(self, message: str):

        # Since Python could not interrupt the OS during the writing of a message,
        # we could not the message writing cross midnight.
        # The code here would only start a new date when the message starts writing on a new day

        log_path = self._get_file_path()
        with open(log_path, "a") as file:
            file.write(message)