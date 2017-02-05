#!/usr/local/bin/python3.6
import time
import sched
from datetime import datetime, timedelta, date
import asyncio
import functools
import sys
import math

def sayhi():
    print("hello")

class Scheduler:
    def __init__(self):
        self.q = []
    def enter_after(self, seconds_delay, callback):
        self.q.append(Timedelta(seconds_delay))
    def get_last(self):
        if self.q:
            return self.q[len(self.q)]
        return Timedelta(20)
    def last_exit(self):
        prev_delay = self.get_last()
        return prev_delay.get_timestamp()
    def schedule_next(self):
        delay = Poisson.generate()
        self.enter_after(delay.to_seconds(),sayhi)

class Timedelta:
    def __repr__(self):
        my_repr = "".join(["Sleep from: ", self.get_start_time().strftime("%c"), "\n",
                   "Seconds: ",str(self.to_seconds()),"\n",
                   "Wake at: ", self.to_datetime().strftime("%c"),"\n"])
        return my_repr
    def __init__(self, value, start_time=datetime.now()):
        self.start = start_time
        self.val = timedelta(seconds=value)
        self.callback = None
    def get_start_time(self):
        return self.start
    def get_timedelta(self):
        return self.val
    def to_seconds(self):
        return int(self.val.total_seconds())
    def to_datetime(self):
        return self.start + self.val

class Poisson():
    def generate(rate_parameter=1/90.0):
        dt = -math.log(1.0 - random.random()) / (rate_parameter)
        timedelta_obj = Timedelta(timedelta(seconds=dt).total_seconds())
        return timedelta_obj



# class Scheduler():
#
#     def clear_all(self):
#         self.frozen = 0
#         self.dt = 0
#         self.next_arrival = 0
#     def freeze(self):
#         self.frozen = datetime.now()
#     def started_at(self):
#         if self.frozen is 0:
#             self.frozen = date.now()
#         return self.frozen
#     def get_current_time(self):
#         return datetime.now()
#     def get_next_arrival(self):
#         if self.next_arrival is 0:
#             self.next_arrival  = self.calculate_next_arrival()
#         return self.next_arrival
#     def format(self, datetime_object):
#         assert(isinstance(datetime_object, datetime))
#         return datetime_object.strftime("%c")
#     def get_formatted_current_time(self):
#         return self.get_current_time().strftime("%c")
#     def get_formatted_next_arrival(self):
#         return self.get_current_time().strftime("%c")
#     def get_timedelta(self):
#         if self.dt is 0:
#             dt = -math.log(1.0 - random.random()) / self.rate_parameter
#             self.dt = timedelta(minutes=dt)
#         return self.dt
#     def sleep(self):
#         pass
#     def calculate_next_arrival(self):
#         if self.next_arrival is 0:
#             self.next_arrival  = self.get_timedelta() + self.get_current_time()
#         return self.next_arrival
#         import asyncio
#         import functools
#
#         import asyncio

import random

@asyncio.coroutine
def random_sleep(counter):
    print("{} sleeps for {:.2f} seconds".format(counter, delay))
    yield from asyncio.sleep(delay)
    print("{} awakens".format(counter))

@asyncio.coroutine
def random_sleep(counter,rate_parameter):
    delay = Poisson.generate(1/1.2).to_seconds() * 5
    print("{} sleeps for {:.2f} seconds".format(counter, delay))
    yield from asyncio.sleep(delay)
    print("{} awakens".format(counter))

@asyncio.coroutine
def sleeper(threadcount, rate_parameter):
       print("Creating five tasks")
       tasks = [random_sleep(1,1/1.2) for i in range(0,threadcount)]
       print("Sleeping after starting five tasks")
       print("Waking and waiting for five tasks")
       yield from asyncio.wait(tasks)

@asyncio.coroutine
def do_my_task():
    print("BEER")


class DateProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.exit_future.set_result(True)

@asyncio.coroutine
def get_date(loop):
    code = 'import datetime; print(datetime.datetime.now())'
    exit_future = asyncio.Future(loop=loop)

    # Create the subprocess controlled by the protocol DateProtocol,
    # redirect the standard output into a pipe
    create = loop.subprocess_exec(lambda: DateProtocol(exit_future),
                                  sys.executable, '-c', code,
                                  stdin=None, stderr=None)
    transport, protocol = yield from create

    # Wait for the subprocess exit using the process_exited() method
    # of the protocol
    yield from exit_future

    # Close the stdout pipe
    transport.close()

    # Read the output which was collected by the pipe_data_received()
    # method of the protocol
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()

@asyncio.coroutine
def main_loop(times):
    # while True:
    for _ in range(times):
        yield from asyncio.sleep(5)
        yield from do_my_task()

if __name__ == '__main__':
    s  = Scheduler()
    delay = Poisson.generate()
    s.schedule_next()
    # process = Scheduler()
    # asyncio.get_event_loop().run_until_complete(sleeper(1,1/1.2))
    asyncio.get_event_loop().run_until_complete(main_loop(4))
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    date = loop.run_until_complete(get_date(loop))
    print("Current date: %s" % date)
    loop.close()

    # print("Done five tasks")

# scheduler = sched.scheduler(Process.get_current_time, time.sleep)
# def print_event(name):
#     print('EVENT:', Process.get_formatted_current_time(), name)
#
# Throttle.w

# print('START:', time.time)
# scheduler.enter(2, 1, print_event, ('first',))
# scheduler.enter(3, 1, print_event, ('second',))
#
# scheduler.run()
