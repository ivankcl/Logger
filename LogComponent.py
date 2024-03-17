from datetime import datetime
import os

class LogComponent():

    log_folder = 'Log'

    def __init__(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.folder)


    def write(self, message: str):
        log_name = f'log_{datetime.now().strftime("%Y%m%d")}.txt'
        log_path = os.path.join(self.log_folder, log_name)
        with open(log_path, "a") as file:
            file.write(message)
        
if __name__ == '__main__':
    logComponent = LogComponent()
    logComponent.write('Hello World' + '\n')