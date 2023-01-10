import threading
import serial
import time


class MySerialWorker(object):
    pending_commands = []  # just commands
    pending_queries = []  # commands awaiting responses

    def __init__(self, *args, **kwargs):
        # you might actually need to create this in the thread spawned later
        self.ser = serial.Serial(*args, **kwargs)

    def send_command(self, cmd):
        self.pending_commands.append(cmd)

    def query_command(self, cmd, callback):
        self.pending_queries.append([cmd, callback])

    def _do_query(self, cmd):
        self.ser.write(cmd.encode())
        time.sleep(0.01)  # give it a second
        return self.ser.readline()  # since you are expecting a newline at end of response

    def main_loop(self):
        while self.ser.isOpen():
            while self.pending_queries:  # handle these first
                cmd, callback = self.pending_queries.pop(0)
                callback(cmd, self._do_query(cmd))

            if self.ser.inWaiting():  # check for any pending incoming messages
                message_from_arduino = self.ser.readline()
                print("Arduino says:", message_from_arduino)
            while self.pending_commands:  # send any commands we want
                # write any pending commands
                self.ser.write(self.pending_commands.pop(0))
            time.sleep(0.01)  # sleep a tick

    def run_threaded(self):
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.start()

    def terminate(self):
        self.ser.close()  # closing the port will make the loop exit
        self.thread.join()  # wait for thread to exit


class MainProgram():
    def __init__(self):
        self.ser = MySerialWorker('/dev/ttyACM0', baudrate=9600, timeout=2)
        self.pending_command = False

    def on_result(self, cmd, result):
        print("Device responded to %r with %r" % (cmd, result))
        self.pending_command = False

    def main_loop(self):
        self.ser.run_threaded()
        while True:
            if not self.pending_command:
                # await a command
                cmd = input("SENDQUERY>")
                self.pending_command = True
                self.ser.query_command(cmd=cmd+"\n", callback=self.on_result)
            time.sleep(0.01)  # sleep a tick


MainProgram().main_loop()
