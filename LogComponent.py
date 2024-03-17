from datetime import datetime

class LogComponent():

    def __init__(self):
        pass


    def write(self, message: str):
        log_name = f'log_{datetime.now().strftime("%Y%m%d")}.txt'
        with open(log_name, "a") as file:
            file.write(message + '\n')
        