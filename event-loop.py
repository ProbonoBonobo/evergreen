#!/usr/local/bin/python3

import datetime
import time
import math
import random
from subprocess import call

class TimedEvent:
   def __init__(self, endtime, callback):
       self.endtime = endtime
       self.callback = callback
   def ready(self):
       return self.endtime <= datetime.datetime.now()
class Timer:
   def __init__(self):
       self.events = []
   def call_after(self, delay, callback):
       end_time = datetime.datetime.now() + \
               datetime.timedelta(seconds=delay)
       self.events.append(TimedEvent(end_time, callback))
   def run(self):
       while True:
           ready_events = (e for e in self.events if e.ready())
           for event in ready_events:
               event.callback(self)
               self.events.remove(event)
           time.sleep(0.5)

def format_time(message, *args):
   now = datetime.datetime.now().strftime("%I:%M:%S")
   print(message.format(*args, now=now))
def one(timer):
   format_time("{now}: Called One")
def two(timer):
   format_time("{now}: Called Two")
def three(timer):
   format_time("{now}: Called Three")

class Timedelta:
   def __repr__(self):
       my_repr = "".join(["Sleep from: ", self.get_start_time().strftime("%c"), "\n",
                  "Seconds: ",str(self.to_seconds()),"\n",
                  "Wake at: ", self.to_datetime().strftime("%c"),"\n"])
       return my_repr
   def __init__(self, value, start_time=datetime.datetime.now()):
       self.start = start_time
       self.val = datetime.timedelta(seconds=value)
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
       timedelta_obj = Timedelta(datetime.timedelta(minutes=dt).total_seconds())
       return timedelta_obj

class Repeater:
   def __init__(self):
       self.count = 0
       self.on_wakeup = lambda: call(['/usr/local/bin/python3', '/Users/kz/Projects/Evergreen4/update-git.py'])
   def repeater(self, timer):
       format_time("{now}: repeat {0}", self.count)
       self.count += 1
       self.on_wakeup()
       next_update = Poisson.generate(1/90.0)
       print("Next update at: "  + str(next_update.to_datetime()))
       timer.call_after(next_update.to_seconds(), self.repeater)

if __name__ == '__main__':
    timer = Timer()
    repeater = Repeater()
    next_update = Poisson.generate(1/90.0)
    print("Next update at: "  + str(next_update.to_datetime()))
    timer.call_after(next_update.to_seconds(), repeater.repeater)
    format_time("{now}: Starting")


    timer.run()
