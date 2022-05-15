from multiprocessing import Process, Array, Value
from time import sleep
from random import random

STOP = -1


class Ticker:
    def __init__(self):
        self.process = None
        self.tickers_array = Array("i", [0]*5)
        self.stop_flag = Value("i", 0)

    def run(self):
        self.process = Process(target=self.ticker)
        self.process.start()

    def ticker(self):
        while True:
            if self.stop_flag.value == STOP:
                print("Process stopping")
                break
            for i in range(len(self.tickers_array)):
                self.tickers_array[i] += self.generate_movement()
            sleep(0.1)

    def stop(self):
        self.stop_flag.value = STOP
        self.process.join()
        self.process.close()
        del self.tickers_array
        del self.stop_flag

    @staticmethod
    def generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement


ticker = Ticker()
