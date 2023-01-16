import threading
from time import time, sleep
from datetime import datetime

import serial


class MySerialWorker(object):
    pending_commands = []
    pending_queries = []

    def __init__(self, *args, **kwargs):
        self.ser = serial.Serial(*args, **kwargs)

    def send_command(self, cmd):
        self.pending_commands.append(cmd)

    def query_command(self, start_time, fd, cmd, callback):
        self.pending_queries.append([start_time, fd, cmd, callback])

    def _do_query(self, cmd):
        self.ser.write(cmd.encode())
        sleep(0.01)
        return self.ser.readlines()

    def main_loop(self):
        while self.ser.isOpen():
            while self.pending_queries:
                start_time, fd, cmd, callback = self.pending_queries.pop(0)
                callback(start_time, fd, cmd, self._do_query(cmd))

            if self.ser.inWaiting():
                _ = self.ser.readlines()
            while self.pending_commands:
                self.ser.write(self.pending_commands.pop(0))
            sleep(0.01)

    def run_threaded(self):
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.start()

    def terminate(self):
        self.ser.close()
        self.thread.join()


class MainProgram():
    def __init__(self):
        self.ser = MySerialWorker('/dev/ttyACM0', baudrate=9600, timeout=2)
        self.filename = datetime.now().strftime("%H:%M:%S") + ".txt"
        self.pending_command = False

    def on_result(self, start_time, fd, cmd, result):
        clean_cmd = cmd.replace("\n", "")
        exec_time = time() - start_time
        print(f"Device responded to {clean_cmd} with {result} in {exec_time}")
        fd.write(f"{exec_time}:{clean_cmd}->{result}\n")
        self.pending_command = False

    def talk_to_device(self, commands_generator):
        i = 0
        self.ser.run_threaded()
        with open(self.filename, 'w') as opened_file:
            self.pending_command = True
            self.ser.query_command(start_time=0.0, fd=opened_file, cmd=" \n", callback=self.on_result)
            sleep(1)  # getting init message from arduino
            cmds = commands_generator()
            while True:
                if self.pending_command is False:
                    if i >= len(cmds):
                        self.ser.terminate()
                        break
                    self.pending_command = True
                    cmd = cmds[i]
                    self.ser.query_command(start_time=time(), fd=opened_file, cmd=cmd + "\n", callback=self.on_result)
                    i += 1

                sleep(0.01)


def get_sa():
    cmds = [f"{chr(i)}s" for i in range(32, 126)]
    return cmds

def get_l():
    cmds = ['?s', ' ']
    return cmds

def generate_all_one_byte_commands():
    cmds = [chr(i) for i in range(256)]
    return cmds


def generate_all_two_byte_commands():
    cmds = [chr(i) + chr(j) for i in range(256) for j in range(256)]
    return cmds


if __name__ == "__main__":
    talker = MainProgram()
    talker.talk_to_device(commands_generator=generate_all_one_byte_commands)
